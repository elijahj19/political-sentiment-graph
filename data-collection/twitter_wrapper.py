import sys
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis')
import my_sentiment_analyzer as msa # this is the sentiment analyzer code from the sentiment-analysis folder

from bluebird import BlueBird
import twint # import Twitter scraper
import json

ABSOLUTE_CACHE_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/data-collection/twitter_cache"

cache = {} # cache of usernames to data

def loadCache():
    print('Finding saved cache')
    try:
        cacheFile = open(f'{ABSOLUTE_CACHE_FOLDER_PATH}/twitter_cache.json')
        global cache 
        cache = json.load(cacheFile)
    except:
        print('No saved cache found or saved cache corrupted')

def saveCache():
    print('Saving cache')
    try:
        f = open(f'{ABSOLUTE_CACHE_FOLDER_PATH}/twitter_cache.json', 'w')
        f.write(json.dumps(cache))
        f.close()
    except:
        print('Could not save cache :(')

def getFollowers(username):
    # check if user is cached already, if so then return followers
    if username in cache and 'followers' in cache[username]:
        print('username is cached')
        return cache[username]['followers']
    
    # perform followers search
    followersObj = BlueBird().get_followers(username)
    followers = []
    for user in followersObj: # user is the user's username
        followers.append(user)

    # save user to cache
    if username in cache:
        cache[username]['followers'] = followers
    else:
        cache[username] = {'followers': followers}

    return followers

def getFollowing(username):
    # check if user is cached already, if so then return following
    if username in cache and 'following' in cache[username]:
        print('username is cached')
        return cache[username]['following']

    # perform following search
    followingObj = BlueBird().get_followings(username)
    following = []
    for user in followingObj: # user is the user's username
        following.append(user)
    
    # save user to cache
    if username in cache:
        cache[username]['following'] = following
    else:
        cache[username] = {'following': following}

    return following

def getFollowersAndFollowingNums(username):
    if username in cache and 'followersNum' in cache[username]:
        return (cache[username]['followersNum'], cache[username]['followingNum'])
    
    users = []
    # Twint might be more efficient at this than Bluebird???
    # perform search
    c = twint.Config()
    c.Username = str(username)
    c.Hide_output = True
    c.Store_object = True # store as object
    c.Store_object_users_list = users
    twint.run.Lookup(c)

    user = users[0]
    followers = int(user.followers)
    following = int(user.following)

    # save user to cache
    if username in cache:
        cache[username]['followersNum'] = followers
        cache[username]['followingNum'] = following
    else:
        cache[username] = {
            'followersNum': followers,
            'followingNum': following
        }
    return (followers, following)

def getUserTweetsAboutTopic(username, topic, limit=100):
    # returned cache value if available
    if username in cache and 'topics' in cache[username] and topic in cache[username]['topics']:
        return cache[username]['topics'][topic]['tweets']
    
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

    # filter tweets to make sure query was correct
    tweets = []
    totalTweets = 0
    for tweet in tweetList:
        if (str(username) == str(tweet.username) and topic in tweet.tweet.lower()):
            if totalTweets >= 20: # for sake of brevity only keep a maximum of 20 tweets
                break
            totalTweets += 1
            tweets.append(tweet.tweet)

    if username in cache and 'topics' in cache[username]:
        cache[username]['topics'][topic] = {
            'tweets': tweets,
            'totalTweets': totalTweets
        }
    elif username in cache:
        cache[username]['topics'] = {
            topic: {
                'tweets': tweets,
                'totalTweets': totalTweets
            }
        }
    else:
        cache[username] = {
            'topics': {
                topic: {
                    'tweets': tweets,
                    'totalTweets': totalTweets
                }
            }
        }

    return tweets


# getUserSentiment
# username (string): the Twitter username of the user
# topic (string): the political topic/person to see if the user is political about
# maxTweets (integer): maximum number of sentimented tweets to analyze 
# DESCRIPTION: this function takes in a username and topic to calculate the User's sentiment towards the topic
# returns (average sentiment towards topic, total tweets about topic)
def getUserSentiment(username, topic, maxTweets = 20):
    # if we already know the sentiment, return it
    if username in cache and 'topics' in cache[username] and topic in cache[username]['topics']:
        return (cache[username]['topics'][topic]['avgSentiment'], cache[username]['topics'][topic]['totalTweets'])
    # if we don't have the tweets then get the tweets
    elif username not in cache or 'topics' not in cache[username] or topic not in cache[username]['topics']:
        getUserTweetsAboutTopic(username, topic)
    
    tweetList = cache[username]['topics'][topic]['tweets']
    avgSentiment = 0 # average sentiment over the tweets analyzed for sentiment
    totalTweets = 0 # total tweets analyzed for sentiment (excludes tweets not analyzed for sentiment)
    for tweet in tweetList:
        calcSentiment = msa.getSentiment(tweet, topic)
        avgSentiment += calcSentiment
        totalTweets += 1

    if totalTweets > 0:
        avgSentiment = avgSentiment / totalTweets

    cache[username]['topics'][topic]['avgSentiment'] = avgSentiment
    cache[username]['topics'][topic]['totalTweets'] = totalTweets

    return (avgSentiment, totalTweets)

