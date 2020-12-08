
## getProbOfConnection
## definitions from https://www.youtube.com/watch?v=rlIJ-g-o8mk
## p = connectance = probability 2 nodes are connected (0<=p<=1)
def getProbOfConnection(graph):
    n = len(graph)
    m = 0
    for node in graph:
        m += node['following']
    p = m / (n*(n-1) / 2) # all edges in graph over all possible edges
    return p

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
