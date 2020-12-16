import sys
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis')

from bluebird import BlueBird
import twint # import Twitter scraper
import json

ABSOLUTE_CACHE_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis/data"

cache = {}
"""
cache = {
    'topic': {
        tweets: ['positiveTweetText', 'positiveTweetText', 'negativeTweet', 'neutralTweet'],
        labels: [1,                     1,                  -1,             0]
    }
}
"""

def loadCache():
    print('Finding saved cache')
    try:
        cacheFile = open(f'{ABSOLUTE_CACHE_FOLDER_PATH}/tweet_sentiment_data.json')
        global cache 
        cache = json.load(cacheFile)
        print('loaded cache')
    except:
        print('No saved cache found or saved cache corrupted')

def saveCache():
    print('Saving cache')
    try:
        f = open(f'{ABSOLUTE_CACHE_FOLDER_PATH}/tweet_sentiment_data.json', 'w')
        f.write(json.dumps(cache))
        f.close()
        print('saved cache')
    except:
        print('Could not save cache :(')

def getTweets(topic, amount = 1000):
    tweetList = []
    c = twint.Config()
    c.Limit = amount # Twint only gets Tweets in the size of 100
    c.Count = True
    c.Retweets = False
    c.Search = topic # contains this keyword of topic
    c.Since = "2020-11-01" # only output tweets since this date
    c.Verified = False # users should not be verified (blue check mark)
    c.Hide_output = True # don't print output to console here (maybe do it elsewhere)
    c.Store_object = True # store as object
    c.Store_object_tweets_list = tweetList
    twint.run.Search(c)

    return [tweet.tweet for tweet in tweetList]

def askAboutTweet(topic, tweet):
    print('---------------------------------------------------------------------------------------')
    print(f'What is the sentiment towards{topic}?')
    print(tweet)
    return int(input(f'Sentiment towards {topic} (-1, 0, 1): '))

def labelTweets(topic):
    if topic not in cache:
        cache[topic] = {
            'tweets': [],
            'labels': []
        }
    tweetList = getTweets(topic)
    for tweet in tweetList:
        label = askAboutTweet(topic, tweet)
        cache[topic]['tweets'].append(tweet)
        cache[topic]['labels'].append(label)
        saveCache()

if __name__ == "__main__":
    topic = input('What topic of tweet do you want to label: ')
    labelTweets(topic)