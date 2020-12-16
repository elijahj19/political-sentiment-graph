import aspect_based_sentiment_analysis as absa
from afinn import Afinn
import sys
import json
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis')

ABSOLUTE_CACHE_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/sentiment-analysis/data"

cache = {}
try:
    cacheFile = open(f'{ABSOLUTE_CACHE_FOLDER_PATH}/tweet_sentiment_data.json')
    cache = json.load(cacheFile)
    print('loaded cache')
except:
    print('No saved cache found or saved cache corrupted')

afinn = Afinn()

nlp = absa.load("absa/classifier-lapt-0.2")

correct = 0
total = 0
wrongTweets = [] #{text: , predicted:, actual:,}
for topic in cache:
    for i in range(len(cache[topic]['tweets'])):
        total += 1
        tweet = cache[topic]['tweets'][i]
        actual = cache[topic]['labels'][i]
        sentimentObj, extraStuff = nlp(tweet, aspects=[topic, topic])
        predicted = 0
        if sentimentObj.sentiment == absa.Sentiment.negative:
            predicted = -1
        elif sentimentObj.sentiment == absa.Sentiment.positive:
            predicted = 1
        else:
            predicted = 0
        
        if predicted != actual:
            wrongTweets.append({
                'text': tweet,
                'predicted': predicted,
                'actual': actual
            })
        else:
            correct += 1

total = total if total > 0 else 1
print(f'Total Accuracy: {correct / total}')
for error in wrongTweets:
    print('-------------------------------------------------------------')
    print(error['text'])
    print(f"Expected {error['actual']}, predicted {error['predicted']}")
