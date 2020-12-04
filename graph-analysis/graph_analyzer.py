

def calculateHomophily(graph):
    pass

def getPosNegNeutNodes(graph):
    posNodes = 0
    negNodes = 0
    neutNodes = 0
    for user in graph:
        if graph[user]['topicAvgSentiment'] > 0:
            posNodes += 1
        elif graph[user]['topicAvgSentiment'] < 0:
            negNodes += 1
        else:
            neutNodes += 1
    return (posNodes, negNodes, neutNodes)
