## this program will use graph_generator.py to create and save the graphs I want to create

import json
import datetime

import graph_generator as gg

ABSOLUTE_DATA_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/data-collection/data"

def saveGraph(graph, topic, rootUserSentiment, graphType):
    print('saving graph')
    
    graphJSON = json.dumps(graph)
    currentTime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f") # 2020_12_31_13_45_30_000321
    sentiment = "positive" if rootUserSentiment > 0 else "negative"
    f = open(f"{ABSOLUTE_DATA_FOLDER_PATH}/{topic}_{graphType}_{sentiment}_{currentTime}_Graph.json", "w")
    f.write(graphJSON)
    f.close()

# main function that runs when python code is run
if __name__ == "__main__":

    print("graph generator interface main called")
     
    index = 0 
    topic = "trump"
    rootUserSentiment = -1
    frontiers = 4
    minTweets = 2
    graphType = 'getSingleTopicNetworkReverse'
    try: 
        trumpNetwork = gg.createSingleTopicNetwork(topic, rootUserSentiment, graphType, frontiers, minTweets)
        saveGraph(trumpNetwork, topic, rootUserSentiment, graphType)
    except:
        print("Could not create network")
