## Elijah Jasso 2020
## This python code collects and stores tweets

# import sentiment analyzer black box 
import sys
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis')
import my_sentiment_analyzer as msa # this is the sentiment analyzer code from the sentiment-analysis folder

import json

import twint # import Twitter scraper

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
    c = twint.Config()
    c.Username = username
    c.Hide_output = True
    #c.Limit = MAX_FOLLOWERS
    c.Store_object = True
    c.Store_object_follow_list = followers
    twint.run.Followers(c)

    return followers

def getFollowing(username):
    following = []
    # perform Twitter scrape for user's followers
    c = twint.Config()
    c.Username = username
    c.Hide_output = True
    #c.Limit = MAX_FOLLOWING
    c.Store_object = True
    c.Store_object_follow_list = following
    twint.run.Following(c)

    return following

# getUserSentiment
# username (string): the Twitter username of the user
# topic (string): the political topic/person to see if the user is political about
# DESCRIPTION: this function takes in a username and topic to calculate the User's sentiment towards the topic
# returns (average sentiment towards topic, total tweets about topic)
def getUserSentiment(username, topic):
    print(f"Determining user {username}'s sentiment towards {topic}")
    tweetList = []
    c = twint.Config()
    c.Limit = 100 # Twint only gets Tweets in the size of 100
    c.Username = str(username)
    c.Count = True
    c.Retweets = False
    c.Search = topic # contains this keyword of topic
    c.Store_object = True # store as object
    c.Store_object_tweets_list = tweetList
    c.Hide_output = True
    twint.run.Search(c)

    avgSentiment = 0
    totalTweets = 0
    for tweet in tweetList:
        if totalTweets > 20:
            break
        if (str(username) == str(tweet.username) and topic in tweet.tweet.lower()):
            calcSentiment = msa.getSentiment(tweet.tweet, topic)
            avgSentiment += calcSentiment
            totalTweets += 1
        
    if totalTweets > 0:
        avgSentiment = avgSentiment / totalTweets
    print(f"{username} has {avgSentiment} sentiment towards {topic} over {totalTweets} tweets")
    return (avgSentiment, totalTweets)

def filterFollowList(followList, topic, minTweets = 2):
    filteredList = []
    for user in followList:
        if not isUserValid(user):
            continue
        avgSentiment, totalTweets = getUserSentiment(user, topic)
        if (avgSentiment != 0) and totalTweets > minTweets:
            filteredList.append(user)
    return filteredList


# getUsers
# frontiers (integer): how many BFS frontiers from starting user to get
def getUserMap(rootUsername, topic, frontiers):
    """
    userMap
    maps username to data
    {
        "username1": { # username 1
            topicAvgSentiment: 1,
            topicTotalTweets: 10
            followerIDs: [2, 3, 10],
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
    userMap = {}
    

    return userMap

# minTweets helps to minimize error caused by faulty sentiment analysis
def getInitialUser(topic, desiredSentiment, minTweets = 2):
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
    return initialUser

# createSingleTopicNetwork
# topic (string): political topic focus of network
# initialUserSentiment (integer): should the root node user of the network/graph have positive (>0) or negative (<0)
#  sentiment towards topic
# fronters (integer): how many BFS frontiers starting from the root node should there be 
def createSingleTopicNetwork(topic, initialUserSentiment, frontiers = 1, minTweets = 2):
    print(f"Creating graph about {topic} with {frontiers} frontiers")
    rootUser = getInitialUser(topic, initialUserSentiment, minTweets)
    # if unable to get a root user
    if rootUser == None:
        raise Exception(f"Could not find suitable root user for topic {topic} with {initialUserSentiment} sentiment")
    print(f"root user node is {rootUser}")
    print(getFollowers(rootUser["username"]))
    print(getFollowing(rootUser["username"]))
    #getUserMap(rootUser["username"], topic, frontiers)


# main function that runs when python code is run
if __name__ == "__main__":
    print("main called")
    positiveTrumpNetwork = createSingleTopicNetwork("trump", 1, 2)
    #print(getFollowers(1010236118))
    # negativeTrumpNetwork = createSingleTopicNetwork("trump", -1, 1, 2)

    # positiveBidenNetwork = createSingleTopicNetwork("biden", 1, 1, 2)
    # negativeBidenNetwork = createSingleTopicNetwork("biden", -1, 1, 2)