## Elijah Jasso 2020
## This python code creates the topic sentiment graph

# import sentiment analyzer black box 
import sys
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis')
import my_sentiment_analyzer as msa # this is the sentiment analyzer code from the sentiment-analysis folder
import twitter_wrapper as tw

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
    followers, following = tw.getFollowersAndFollowingNums(username)
    print(f"{username}  has {followers} followers and is following {following} users")
    isValid = (followers <= MAX_FOLLOWERS and following <= MAX_FOLLOWING and followers >= MIN_FOLLOWERS and following >= MIN_FOLLOWING)
    return isValid

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
            tempFollowing = tw.getFollowing(username) # get all followers
            
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
                avgSentiment, totalTweets = tw.getUserSentiment(followingUser, topic)
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
            avgSentiment, totalTweets = tw.getUserSentiment(tweet.username, topic)

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
    print(tw.getFollowers(rootUser["username"]))
    print(tw.getFollowing(rootUser["username"]))
    #getUserMap(rootUser["username"], topic, frontiers)

    network = getSingleTopicNetwork(rootUser["username"], rootUser["avgSentiment"], rootUser["totalTweets"], topic, frontiers)

    return network


# main function that runs when python code is run
if __name__ == "__main__":
    print("main called")
    positiveTrumpNetwork = createSingleTopicNetwork("trump", 1, 2)