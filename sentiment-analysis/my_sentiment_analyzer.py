# This is the black box sentiment analyzer which will be used by the data processor and uses some other sentiment analysis method

import preprocessor as p
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.MENTION) # filter out urls, emojis and mentions (@'s)

import aspect_based_sentiment_analysis as absa
nlp = absa.load()

# getSentiment(text: string, idea: string)
# This function accepts some text, and an idea/entity for which the function should extract the sentiment about
# returns a number between -3 and 3 to determine sentiment, where -3 is very negative, 0 is neutral, and 3 is very positive
def getSentiment(text, idea):
    #print(f'Attempting to analyze text for {idea}')
    sentimentObj, extraStuff = nlp(text, aspects=[idea, idea])
    if sentimentObj.sentiment == absa.Sentiment.negative:
        return -1
    elif sentimentObj.sentiment == absa.Sentiment.positive:
        return 1
    else:
        return 0

#getSentiment("trump is the worst", "trump")