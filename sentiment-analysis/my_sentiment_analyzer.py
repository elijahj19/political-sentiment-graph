# This is the black box sentiment analyzer which will be used by the data processor and uses some other sentiment analysis method

import aspect_based_sentiment_analysis as absa
nlp = absa.load("absa/classifier-lapt-0.2")

# getSentiment(text: string, idea: string)
# This function accepts some text, and an idea/entity for which the function should extract the sentiment about
# returns a number between -1 and 1 to determine sentiment
def getSentiment(text, idea):
    #print(f'Attempting to analyze text for {idea}')
    sentimentObj, extraStuff = nlp(text, aspects=[idea, idea])
    if sentimentObj.sentiment == absa.Sentiment.negative:
        return -1
    elif sentimentObj.sentiment == absa.Sentiment.positive:
        return 1
    else:
        return 0