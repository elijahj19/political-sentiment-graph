import aspect_based_sentiment_analysis as absa

nlp = absa.load()
text = ("I hate Biden")

trump, biden = nlp(text, aspects=['trump', 'biden'])
#assert price.sentiment == absa.Sentiment.negative
#assert slack.sentiment == absa.Sentiment.positive

print(trump.sentiment)
print(biden.sentiment)