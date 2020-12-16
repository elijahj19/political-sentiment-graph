import copy
import json
import sys


ABSOLUTE_CONSOLIDATED_DATA_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/data-collection/consolidated_data/data.json"
ABSOLUTE_ANALYZED_GRAPHS_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/graph-analysis/analyzed_graphs/analzyed_graphs.json"
## getProbOfConnection
## definitions from https://www.youtube.com/watch?v=rlIJ-g-o8mk
## p = connectance = probability 2 nodes are connected (0<=p<=1)
def getProbOfConnection(graph):
    n = len(graph) # number of nodes
    m = 0 # number of edges (initialized to 0)
    for node in graph:
        m += len(graph[node]['following']) # add the degree of the node to m
    possibleEdges = n * (n-1) # the amount of edges possible in a directed graph
    p = m / (possibleEdges if possibleEdges > 0 else 1)
    return p    

def calculateHomophily(graph):
    pass

# get the amount of positive, negative, and neutral nodes in the graph
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

# get the dyadicity (expected connections between same sentiment nodes / actual connections between same sentiment nodes)
def getDyadicity(graph):
    n = len(graph)
    p = getProbOfConnection(graph) # get p = connectance= probably 2 nodes have a connection (directed from u to v)
    posNodes, negNodes, _ = getPosNegNeutNodes(graph)

    # expected number of connections between same sentiment nodes
    posExpected = posNodes * (posNodes - 1) * p
    negExpected = negNodes * (negNodes - 1) * p

    # calculate the actual number of connections between same sentiment nodes
    posActual = 0
    negActual = 0
    for user in graph:
        userSentiment = graph[user]['topicAvgSentiment']
        for follower in graph[user]['followers']:
            if graph[follower]['topicAvgSentiment'] * userSentiment > 0: # if the sentiments are of the same sign
                if userSentiment < 0:
                    negActual += 1
                else:
                    posActual += 1
    
    posDyadicity = posActual / (posExpected if posExpected > 0 else 0.0000001)
    negDyadicity = negActual / (negExpected if negExpected > 0 else 0.0000001)
    return (posDyadicity, negDyadicity)

# get the average sentiment for users in the graph
def getAvgSentiment(graph):
    sumSentiment = 0
    for user in graph:
        sumSentiment += graph[user]['topicAvgSentiment']
    return sumSentiment / len(graph)

# density is m / n (m = num of edges, n = number of nodes), source On Finding Dense Subgraphs" by Samir Khuller and Barna Saha
def getGraphDensity(graph):
    edges = 0
    n = len(graph) if len(graph) > 0 else 1
    for user in graph:
        edges += len(graph[user]['followers']) + len(graph[user]['following'])
    return edges / n

# Algorithm 2.2: DENSEST-SUBGRAPH-DIRECTED(G = (V, E)) from "On Finding Dense Subgraphs" by Samir Khuller and Barna Saha
def getDensestSubgraph(graph):
    # H = [copy.deepcopy(graph)] # 2*n length array of copies of graph
    # density = []
    # i = 0
    # n = len(graph)
    # while len(H[i]) > 0 and i < 2 * n:
    #     print(H[i])
    #     userLowestInDegName = ''
    #     userLowestInDegNum = 99999999999
    #     userLowestOutDegName = ''
    #     userLowestOutDegNum = 9999999999
    #     lowestDegUser = ''
    #     category = '' # other users reference to v
    #     for user in H[i]:
    #         if len(H[i][user]['followers']) == 0 and len(H[i][user]['following']) == 0:
    #             pass
    #         if len(H[i][user]['followers']) < userLowestInDegNum:
    #             userLowestInDegName = user
    #             userLowestInDegNum = len(H[i][user]['followers'])
    #         if len(H[i][user]['following']) < userLowestOutDegNum:
    #             userLowestOutDegName = user
    #             userLowestOutDegNum = len(H[i][user]['following'])
    #     # if userLowestInDegNum < userLowestOutDegNum:
    #     #     lowestDegUser = userLowestInDegName
    #     #     if userLowestInDegNum == 0:
    #     #         lowestDegUser = userLowestOutDegName
    #     #     category = 'following'
    #     #     H[i][lowestDegUser]['followers'] = []
    #     # else:
    #     #     lowestDegUser = userLowestOutDegName
    #     #     if userLowestOutDegNum == 0:
    #     #         lowestDegUser = userLowestInDegName
    #     #     category = 'followers'
    #     #     H[i][lowestDegUser]['following'] = []
    #     # for user in H[i]:
    #     #     if lowestDegUser in H[i][user][category]:
    #     #         H[i][user][category].remove(lowestDegUser)
    #     # if len(H[i][lowestDegUser]['followers']) == 0 and len(H[i][lowestDegUser]['followers']) == 0:
    #     #     del H[i][lowestDegUser]
    #     #     for user in H[i]:
    #     #         for cat in ['followers', 'following']:
    #     #             if lowestDegUser in H[i][user][cat]:
    #     #                 H[i][user][cat].remove(lowestDegUser)
    #     if userLowestInDegNum < userLowestOutDegNum:
    #         lowestDegUser = userLowestInDegName
    #         category = 'following'
    #         H[i][lowestDegUser]['followers'] = []
    #     else:
    #         lowestDegUser = userLowestOutDegName
    #         category = 'followers'
    #         H[i][lowestDegUser]['following'] = []
    #     for user in H[i]:
    #         for cat in ['followers', 'following']:
    #             if lowestDegUser in H[i][user][cat]:
    #                 H[i][user][cat].remove(lowestDegUser)
    #     del H[i][lowestDegUser]
        
    #     copiedHi = {}
    #     for thing in H[i]:
    #         copiedHi[thing] = copy.deepcopy(H[i][thing])
    #     H.append(copy.deepcopy(copiedHi))
    #     density.append(getGraphDensity(H[i]))
    #     i += 1
    # indexOfDensest = density.index(max(density))
    return graph

# returns (amount of positive -> positive, amount of negative -> negative, amount of positive -> negative, amount of negative -> positive)
def getEdgeRelationships(graph):
    posToNeg = 0
    negToPos = 0
    posToPos = 0
    negToNeg = 0
    for user in graph:
        for follower in graph[user]['followers']:
            if graph[user]['topicAvgSentiment'] > 0 and graph[follower]['topicAvgSentiment'] > 0:
                posToPos += 1
            elif graph[user]['topicAvgSentiment'] > 0 and graph[follower]['topicAvgSentiment'] < 0:
                negToPos += 1
            elif graph[user]['topicAvgSentiment'] < 0 and graph[follower]['topicAvgSentiment'] > 0:
                posToNeg += 1
            else:
                negToNeg += 1
    
    return (posToPos, negToNeg, posToNeg, negToNeg)

if __name__ == "__main__":
    testGraph1 = {
                "ginnyclausen": {
                    "topicAvgSentiment": -1,
                    "topicTotalTweets": 20,
                    "followers": ["nurankaraca80", "pstone3504", "cocoajohnston", "dustoff_54", "avesi", "nothingbutrabb1", "laurenbakerfit", "torpeto", "sudburyfrob", "ferretkit", "cburns186", "hemi66coronet", "kathyharris44", "dustinmcd123", "jfdiv41"],
                    "following": []
                },
                "nurankaraca80": {
                    "topicAvgSentiment": -0.85,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "pstone3504": {
                    "topicAvgSentiment": -0.75,
                    "topicTotalTweets": 4,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "cocoajohnston": {
                    "topicAvgSentiment": -0.65,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "dustoff_54": {
                    "topicAvgSentiment": -0.5,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "avesi": {
                    "topicAvgSentiment": -0.75,
                    "topicTotalTweets": 4,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "nothingbutrabb1": {
                    "topicAvgSentiment": -0.55,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "laurenbakerfit": {
                    "topicAvgSentiment": -0.42857142857142855,
                    "topicTotalTweets": 7,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "torpeto": {
                    "topicAvgSentiment": -0.3,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "sudburyfrob": {
                    "topicAvgSentiment": -0.631578947368421,
                    "topicTotalTweets": 19,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "ferretkit": {
                    "topicAvgSentiment": -0.6,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "cburns186": {
                    "topicAvgSentiment": -0.55,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "hemi66coronet": {
                    "topicAvgSentiment": -0.7,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "kathyharris44": {
                    "topicAvgSentiment": -0.4,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "dustinmcd123": {
                    "topicAvgSentiment": -0.65,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                },
                "jfdiv41": {
                    "topicAvgSentiment": -0.8,
                    "topicTotalTweets": 20,
                    "following": ["ginnyclausen"],
                    "followers": []
                }
            }
    # dg = getDensestSubgraph(testGraph1)
    # print('---------------------------------')
    # print(dg)
    # raise 'error'
    print('Finding consolidated graphs')
    graphs = []
    try:
        cacheFile = open(f'{ABSOLUTE_CONSOLIDATED_DATA_PATH}')
        graphs = json.load(cacheFile)
    except:
        print('Cannot load consolidated graphs')
        raise "cannot load consolidated graphs"
    
    analyzedGraphs = {}
    for topic in graphs:
        analyzedGraphs[topic] = {
            'allStats': {
                'seenGraphs': 0,
                'avgSentiment': 0,
                'avgPosDyadicity': 0,
                'avgNegDyadicity': 0,
                'avgPercentNodesPos': 0,
                'avgPercentNodesNeg': 0,
                'avgGraphDensity': 0,
                'avgDensestSubgraphSize': 0,
                'avgDensestSubgraphDensity': 0,
                'avgSize': 0
            },
            'positiveStats': { # stats for positive majority graphs
                'seenGraphs': 0,
                'avgSentiment': 0,
                'avgPosDyadicity': 0,
                'avgNegDyadicity': 0,
                'avgPercentNodesPos': 0,
                'avgPercentNodesNeg': 0,
                'avgGraphDensity': 0,
                'avgDensestSubgraphSize': 0,
                'avgDensestSubgraphDensity': 0,
                'avgSize': 0
            },
            'negativeStats': { # stats for negative majority graphs
                'seenGraphs': 0,
                'avgSentiment': 0,
                'avgPosDyadicity': 0,
                'avgNegDyadicity': 0,
                'avgPercentNodesPos': 0,
                'avgPercentNodesNeg': 0,
                'avgGraphDensity': 0,
                'avgDensestSubgraphSize': 0,
                'avgDensestSubgraphDensity': 0,
                'avgSize': 0
            },
            'graphs': []
        }
    
    for topic in graphs:
        for graph in graphs[topic]['graphs']:
            pos, neg, neut = getPosNegNeutNodes(graph)
            statsString = ''
            if pos > neg:
                statsString = 'positiveStats'
            else:
                statsString = 'negativeStats'
            
            avgSentiment = getAvgSentiment(graph)
            print('finding graph density')
            graphDensity = getGraphDensity(graph)
            print('finding densest subgraph')
            densestSubgraph = getDensestSubgraph(graph)
            print('finding densest subgrpah density')
            densestSubgraphDensity = getGraphDensity(densestSubgraph)

            analyzedGraphs[topic][statsString]['seenGraphs'] += 1
            analyzedGraphs[topic][statsString]['avgSentiment'] += avgSentiment
            posD, negD = getDyadicity(graph)
            analyzedGraphs[topic][statsString]['avgPosDyadicity'] += posD
            analyzedGraphs[topic][statsString]['avgNegDyadicity'] += negD
            analyzedGraphs[topic][statsString]['avgPercentNodesPos'] += pos / (pos + neg)
            analyzedGraphs[topic][statsString]['avgPercentNodesNeg'] += neg / (pos + neg)
            analyzedGraphs[topic][statsString]['avgDensestSubgraphSize'] += len(densestSubgraph)
            analyzedGraphs[topic][statsString]['avgDensestSubgraphDensity'] += densestSubgraphDensity
            analyzedGraphs[topic][statsString]['avgGraphDensity'] += graphDensity
            analyzedGraphs[topic][statsString]['avgSize'] += len(graph)

            analyzedGraphs[topic]['allStats']['seenGraphs'] += 1
            analyzedGraphs[topic]['allStats']['avgSentiment'] += avgSentiment
            analyzedGraphs[topic]['allStats']['avgPosDyadicity'] += posD
            analyzedGraphs[topic]['allStats']['avgNegDyadicity'] += negD
            analyzedGraphs[topic]['allStats']['avgPercentNodesPos'] += pos / (pos + neg)
            analyzedGraphs[topic]['allStats']['avgPercentNodesNeg'] += neg / (pos + neg)
            analyzedGraphs[topic]['allStats']['avgDensestSubgraphSize'] += len(densestSubgraph)
            analyzedGraphs[topic]['allStats']['avgDensestSubgraphDensity'] += densestSubgraphDensity
            analyzedGraphs[topic]['allStats']['avgGraphDensity'] += graphDensity
            analyzedGraphs[topic]['allStats']['avgSize'] += len(graph)

            analyzedGraphs[topic]['graphs'].append({
                'posNodes': pos,
                'negNodes': neg,
                'avgSentiment': avgSentiment,
                'posDyadicity': posD,
                'negDyadicity': negD,
                'nodesPos': pos / (pos + neg),
                'nodesNeg': neg / (pos + neg),
                'graphDensity': graphDensity,
                'densestSubgraphSize': len(densestSubgraph),
                'graph': graph,
                'densestSubset': densestSubgraph
            })
    for topic in analyzedGraphs:
        for statsType in ['positiveStats', 'negativeStats']:
            analyzedGraphs[topic][statsType]['avgSentiment'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgPosDyadicity'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgNegDyadicity'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgPercentNodesPos'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgPercentNodesNeg'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgDensestSubgraphSize'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgDensestSubgraphDensity'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgGraphDensity'] /= analyzedGraphs[topic][statsType]['seenGraphs']
            analyzedGraphs[topic][statsType]['avgSize'] /= analyzedGraphs[topic][statsType]['seenGraphs']

        analyzedGraphs[topic]['allStats']['avgSentiment'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgPosDyadicity'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgNegDyadicity'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgPercentNodesPos'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgPercentNodesNeg'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgDensestSubgraphSize'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgDensestSubgraphDensity'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgGraphDensity'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
        analyzedGraphs[topic]['allStats']['avgSize'] /= analyzedGraphs[topic]['allStats']['seenGraphs']
    print('saving analyzed graphs')
    try:
        f = open(f'{ABSOLUTE_ANALYZED_GRAPHS_PATH}', 'w')
        f.write(json.dumps(analyzedGraphs))
        f.close()
    except:
        print('Could not save analyzed graphs :(')

