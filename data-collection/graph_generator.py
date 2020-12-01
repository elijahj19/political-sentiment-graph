## Elijah Jasso 2020
## This python code creates the topic sentiment graph

# import sentiment analyzer black box 
import sys
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis')
import my_sentiment_analyzer as msa # this is the sentiment analyzer code from the sentiment-analysis folder

import json

import twint # import Twitter scraper
from bluebird import BlueBird # for getting followers and following, since Twint has a bug

# global variables
MAX_FOLLOWERS = 450 # maximum amount of followers a user can have to qualify
MIN_FOLLOWERS = 10 # minimum amount of followers a user can have to qualify
MAX_FOLLOWING = 1000 # maximum amount of users a user can follow to qualify
MIN_FOLLOWING = 10 # minimum amount of of users a user can follower to qualify

# isUserValid
# username: the Twitter username of user
# returns True if the user's following and followers conforms to the MAX_FOLLOWERS MIN_FOLLOWERS constraints
# returns False otherwise
def isUserValid(username):
    users = []
    # perform Twitter scrape of user
    c = twint.Config()
    c.Username = str(username)
    c.Hide_output = True
    c.Store_object = True # store as object
    c.Store_object_users_list = users
    twint.run.Lookup(c)

    # perform validation check
    user = users[0]
    followers = int(user.followers)
    following = int(user.following)
    print(f"{username} is {user.username} has {user.followers} followers and is following {following} users")
    isValid = (followers <= MAX_FOLLOWERS and following <= MAX_FOLLOWING and followers >= MIN_FOLLOWERS and following >= MIN_FOLLOWING)
    return isValid

def getFollowers(username):
    followers = []
    # perform Twitter scrape for user's followers
    # c = twint.Config()
    # c.Username = username
    # c.Hide_output = True
    # #c.Limit = MAX_FOLLOWERS
    # c.Store_object = True
    # c.Store_object_follow_list = followers
    # twint.run.Followers(c)

    followersObj = BlueBird().get_followers(username)

    for u in followersObj:
        followers.append(u)

    return followers

def getFollowing(username):
    following = []
    # perform Twitter scrape for user's followers
    # c = twint.Config()
    # c.Username = username
    # c.Hide_output = True
    # #c.Limit = MAX_FOLLOWING
    # c.Store_object = True
    # c.Store_object_follow_list = following
    # twint.run.Following(c)

    followingObj = BlueBird().get_followings(username)

    for u in followingObj:
        following.append(u)

    return following

def getUserTweetsAboutTopic(username, topic, limit = 100):
    tweetList = []
    c = twint.Config()
    c.Limit = limit
    c.Username = str(username)
    c.Count = True
    c.Retweets = False
    c.Search = topic # contains this keyword of topic
    c.Store_object = True # store as object
    c.Store_object_tweets_list = tweetList
    c.Hide_output = True
    twint.run.Search(c)
    
    return tweetList


# getUserSentiment
# username (string): the Twitter username of the user
# topic (string): the political topic/person to see if the user is political about
# maxTweets (integer): maximum number of sentimented tweets to analyze 
# DESCRIPTION: this function takes in a username and topic to calculate the User's sentiment towards the topic
# returns (average sentiment towards topic, total tweets about topic)
def getUserSentiment(username, topic, maxTweets = 20):
    print(f"Determining user {username}'s sentiment towards {topic}")
    tweetList = getUserTweetsAboutTopic(username, topic, 100)

    avgSentiment = 0 # average sentiment over the tweets analyzed for sentiment
    totalTweets = 0 # total tweets analyzed for sentiment (excludes tweets not analyzed for sentiment)
    for tweet in tweetList:
        if totalTweets > 20: # for sake of brevity only analyze a maximum of 20 tweets
            break
        if (str(username) == str(tweet.username) and topic in tweet.tweet.lower()):
            calcSentiment = msa.getSentiment(tweet.tweet, topic)
            avgSentiment += calcSentiment
            totalTweets += 1
        
    if totalTweets > 0:
        avgSentiment = avgSentiment / totalTweets
    print(f"{username} has {avgSentiment} sentiment towards {topic} over {totalTweets} tweets")
    return (avgSentiment, totalTweets)


# filter the usernames in a following/followers list such that it only incldues those who are nonfamous and have sentiment about topic
# DEPRECATED for now
def filterFollowList(followList, topic, minTweets = 2):
    filteredList = []
    for user in followList:
        if not isUserValid(user):
            continue
        avgSentiment, totalTweets = getUserSentiment(user, topic)
        if (avgSentiment != 0) and totalTweets > minTweets:
            filteredList.append((user, avgSentiment, totalTweets))
    return filteredList


# getSingleTopicNetwork
# rootUsername (string): user's username from which to base the network around
# topic (string): topic focus of the network (what should the network analyze each users' sentiment about)
# frontiers (integer): how many BFS frontiers from starting user to get (maximum length of path from rootUsername to any other node)
# RETURN: adjacency list in the form of Python dictionary 
#   {"username" : {"avgSentiment": -1, "totalTweets": 10, "following": ["username"], "followers": ["username"]}} 
def getSingleTopicNetwork(rootUsername, rootUserAvgSentiment, rootUserTotalTweets, topic, frontiers):
    """
    network
    maps username to data
    {
        "username1": { # username 1
            topicAvgSentiment: 1,
            topicTotalTweets: 10
            followers: [2, 3, 10],
            followingIDs: [2, 3, 10]
        },
        "username2": {
            topicAvgSentiment: 1,
            topicTotalTweets: 10
            followerIDs: [2, 3, 10],
            followingIDs: [2, 3, 10]
        }
    }
    """
    network = {
        rootUsername: {
            "topicAvgSentiment": rootUserAvgSentiment,
            "topicTotalTweets": rootUserTotalTweets,
            "followers": [],
            "following": []
        }
    }
    nonValidUsernames = set() # set of usernames already explored that have been determined to not be valid, saves calls to Twitter

    # perform a modified BFS from rootUsername to create network
    queue = [(rootUsername, 0)] # a queue for each 
    while len(queue) > 0:
        # pop the user from the queue
        username, curFrontier = queue.pop(0)

        # if the user has been already added as a node to network, must be valid
        # at this point the user's followers have been edited but not the following
        if username in network:
            print("user already present in network")
            tempFollowing = getFollowing(username) # get all followers
            
            for followingUser in tempFollowing:
                # if the followed user is already in the network, just append the usernames to respective lists
                if followingUser in network:
                    network[followingUser]["followers"].append(username)
                    network[username]["following"].append(followingUser)
                    continue                    
                # if followed user is outside the frontiers of the grpah or the followed user is not valid, skip
                elif curFrontier >= frontiers or followingUser in nonValidUsernames or not isUserValid(followingUser):
                    continue
                # otherwise must calculate the stats for the followed user and add them to the network
                avgSentiment, totalTweets = getUserSentiment(followingUser, topic)
                if (avgSentiment != 0) and totalTweets > 2:
                    network[followingUser] = {
                        "topicAvgSentiment": avgSentiment,
                        "topicTotalTweets": totalTweets,
                        "following": [],
                        "followers": []
                    }
                    network[username]["following"].append(followingUser)
                    queue.append((followingUser, curFrontier + 1)) # add the new user to the queue with the frontier
                else:
                    nonValidUsernames.add(followingUser)        
        # if the user has not been seen before and is NOT valid
        else:
            print(f"user {username} not valid")
            nonValidUsernames.add(username)
            continue

        

    return network

# getRootNodeUser
# topic (string): political topic user has tweeted about, basis of the network
# desiredSentiment (number): sentiment user should have (on average) towards topic. <0 for negative, >0 for positive
# minTweets (integer): the minimum number of sentimented tweets the user should have towards a topic, to help further verify
#   their sentiment towards a topic, combat against sentiment analysis error
def getRootNodeUser(topic, desiredSentiment, minTweets = 2):
    print(f"Getting root node user for with sentiment of {desiredSentiment} towards {topic}, corraborated by {minTweets} of their tweets")
    tweetList = []
    c = twint.Config()
    c.Limit = 100 # Twint only gets Tweets in the size of 100
    c.Count = True
    c.Retweets = False
    c.Search = topic # contains this keyword of topic
    c.Since = "2020-11-03" # only output tweets since this date
    c.Verified = False # users should not be verified (blue check mark)
    c.Hide_output = True # don't print output to console here (maybe do it elsewhere)
    c.Store_object = True # store as object
    c.Store_object_tweets_list = tweetList
    twint.run.Search(c)

    initialUser = None
    try:
        for tweet in tweetList:
            print(f"{tweet.datestamp}: User {tweet.username} said '{tweet.tweet}'")
            calcSentiment = msa.getSentiment(tweet.tweet, topic)
            if calcSentiment * desiredSentiment < 0 or not isUserValid(tweet.username): # if the calculated sentiment and desired sentiment are of opposite types
                continue # skip to next tweet
            # otherwise we now check if the user has other tweets confirming their sentiment towards the topic
            avgSentiment, totalTweets = getUserSentiment(tweet.username, topic)

            # if the user's avg sentiment is of the type we want and has at least our minTweets about the topic
            if desiredSentiment * avgSentiment > 0 and totalTweets >= minTweets:
                initialUser = {
                    "username": tweet.username,
                    "user_id": tweet.user_id,
                    "avgSentiment": avgSentiment,
                    "totalTweets": totalTweets
                }
                break
    except:
        print('Probably a rate limit error, saving graph as is')
    return initialUser

# createSingleTopicNetwork
# topic (string): political topic focus of network
# initialUserSentiment (integer): should the root node user of the network/graph have positive (>0) or negative (<0)
#  sentiment towards topic
# frontiers (integer): how many BFS frontiers starting from the root node should there be in the returned network
# RETURN: adjacency list in the form of Python dictionary 
#   {"username" : {"avgSentiment": -1, "totalTweets": 10, "following": ["username"], "followers": ["username"]}} 
def createSingleTopicNetwork(topic, rootUserSentiment, frontiers = 1, minTweets = 2):
    print(f"Creating graph about {topic} with {frontiers} frontiers")
    rootUser = getRootNodeUser(topic, rootUserSentiment, minTweets)
    # if unable to get a root user
    if rootUser == None:
        raise Exception(f"Could not find suitable root user for topic {topic} with {rootUserSentiment} sentiment")
    print(f"root user node is {rootUser}")
    print(getFollowers(rootUser["username"]))
    print(getFollowing(rootUser["username"]))
    #getUserMap(rootUser["username"], topic, frontiers)

    network = getSingleTopicNetwork(rootUser["username"], rootUser["avgSentiment"], rootUser["totalTweets"], topic, frontiers)

    return network


# main function that runs when python code is run
if __name__ == "__main__":
    print("main called")
    positiveTrumpNetwork = createSingleTopicNetwork("trump", 1, 2)