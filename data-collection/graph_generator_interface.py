## this program will use graph_generator.py to create and save the graphs I want to create

import json
import datetime

import graph_generator as gg


def saveGraph(graph, topic, rootUserSentiment):
    print('saving graph')
    
    graphJSON = json.dumps(dict)
    currentTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f") # 2020_12_31_13_45_30_000321
    sentiment = "positive" if rootUserSentiment > 0 else "negative"
    f = open(f"data/{topic}_{sentiment}_{currentTime}_Graph.json","w")
    f.write(graphJSON)
    f.close()

# main function that runs when python code is run
if __name__ == "__main__":

    print("graph generator interface main called")
    
    index = 0
    topic = "trump"
    rootUserSentiment = 1
    frontiers = 1
    minTweets = 2 
    positiveTrumpNetwork = gg.createSingleTopicNetwork(topic, rootUserSentiment, frontiers, minTweets)
    saveGraph(positiveTrumpNetwork, topic, rootUserSentiment)
