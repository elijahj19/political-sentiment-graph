# This is the black box sentiment analyzer which will be used by the data processor and uses some other sentiment analysis method


# getSentiment(text: string, idea: string)
# This function accepts some text, and an idea/entity for which the function should extract the sentiment about
# returns a number between -3 and 3 to determine sentiment, where -3 is very negative, 0 is neutral, and 3 is very positive
def getSentiment(text, idea):
    print(f'Attempting to analyze text for {idea}')
    return 0

getSentiment("cool beans", "beans")