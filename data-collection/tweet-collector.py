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


# getUserPoliticalData
# userID (string): the Twitter ID of the user
# topic (string): the political topic/person to see if the user is political about
# minTweets (integer): the minimum number of tweets that are related to the topic
# maxTweets (integer): the maximum number of tweets about the topic to include in the returned data
# DESCRIPTION: this function takes in a userID, topic, and threshold to see if the user is poltical
# returns None if the user does not have more than min_tweets about the topic or if User has 
# returns a dictionary of the user data otherwise
def getUserPoliticalData(userID, topic, minTweets= 3, maxTweets = 10):
    print(f'Determining whether user {userID} is has at least {minTweets} tweets about {topic}')


    return None

# getUsers
# frontiers (integer): how many BFS frontiers from starting user to get
def getUserMap(rootUserID, topic, frontiers):
    """
    userMap
    maps userID to data
    {
        "1": { # userID 1
            topicData: { # data about different political topics
                "trump": { # example data topic "trump",
                    avgSentiment: -1, # average sentiment of tweets that include the topic
                    numTweets: 10, # number of tweets that include the topic
                },
                "biden": {
                    avgSentiment: 1,
                    numTweets: 5,
                },
            },
            followerIDs: [2, 3, 10],
            followingIDs: [2, 3, 10]
        },
        "2": {
            topicData: {
                "trump": {
                    avgSentiment: 1,
                    numTweets: 10,
                },
                "biden": {
                    avgSentiment: -1,
                    numTweets: 5,
                },
            },
            followerIDs: [1, 4, 10],
            followingIDs: [1, 10]
        }
    }
    """
    userMap = {}

    return userMap

# minTweets helps to minimize error caused by faulty sentiment analysis
def getInitialUser(topic, sentiment, minTweets = 2):
    print(f"Getting root node user for with sentiment of {sentiment} towards {topic}, corraborated by {minTweets} of their tweets")
    c = twint.Config()
    c.Limit = 100 # Twint only gets Tweets in the size of 100
    c.Count = True
    c.Retweets = False
    c.Search = topic # contains this keyword of topic
    c.Since = "2020-11-03" # only output tweets since this date
    c.Verified = False # users should not be verified (blue check mark)
    c.Hide_output = True # don't print output to console here (maybe do it elsewhere)
    c.Store_object = True # store as object
    twint.run.Search(c)
    tweetList = twint.output.tweets_list

    for tweet in tweetList:
        print(f"{tweet.datestamp}: User {tweet.username} said '{tweet.tweet}'")
        userID = tweet.user_id

    return None

# createSingleTopicNetwork
# topic (string): political topic focus of network
# initialUserSentiment (integer): should the root node user of the network/graph have positive (>0) or negative (<0)
#  sentiment towards topic
# fronters (integer): how many BFS frontiers starting from the root node should there be 
def createSingleTopicNetwork(topic, initialUserSentiment, frontiers = 1, minTweets = 2):
    print(f"Creating graph about {topic} with {frontiers} frontiers")
    rootUserID = getInitialUser(topic, initialUserSentiment, minTweets)
    #getUserMap(rootUserID, topic, frontiers)


# main function that runs when python code is run
if __name__ == "__main__":
    print("main called")
    positiveTrumpNetwork = createSingleTopicNetwork("trump", 1, 2)
    # negativeTrumpNetwork = createSingleTopicNetwork("trump", -1, 1, 2)

    # positiveBidenNetwork = createSingleTopicNetwork("biden", 1, 1, 2)
    # negativeBidenNetwork = createSingleTopicNetwork("biden", -1, 1, 2)

    

    

