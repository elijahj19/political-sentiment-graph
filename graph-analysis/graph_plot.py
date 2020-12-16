import plotly.graph_objects as go
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import networkx as nx
import json
import sys

ABSOLUTE_ANALYZED_GRAPHS_DATA_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/graph-analysis/analyzed_graphs/analzyed_graphs.json"
ABSOLUTE_PLOT_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/graph-analysis/graph_plots/"
# returns a plotable graph (G, colorMap)
def getPlotableGraph(graph):
    G = nx.DiGraph()
    G.clear()
    edgesArray = []
    usersArray = []
    colorMap = []
    for user in graph:
        usersArray.append(user)
        if graph[user]['topicAvgSentiment'] > 0:
            colorMap.append('green')
        else:
            colorMap.append('red')
        for follower in graph[user]['followers']:
            edgesArray.append([follower, user])
    
    G.add_nodes_from(usersArray, color='black')
    G.add_edges_from(edgesArray)
    return (G, colorMap)


testGraph = {
    'user1': {
        'topicAvgSentiment': 0.5,
        'followers': ['user2', 'user4'],
        'following': ['user2', 'user3']
    },
    'user2': {
        'topicAvgSentiment': -0.5,
        'followers': ['user1', 'user4'],
        'following': ['user1']
    },
    'user3': {
        'topicAvgSentiment': -0.2,
        'followers': ['user2', 'user4'],
        'following': ['user1']
    }, 
    'user4': {
        'topicAvgSentiment': 1,
        'followers': [],
        'following': ['user1', 'user2', 'user3']
    }
}

if __name__ == "__main__":
    print('Finding consolidated graphs')
    graphs = {}
    try:
        cacheFile = open(f'{ABSOLUTE_ANALYZED_GRAPHS_DATA_PATH}')
        graphs = json.load(cacheFile)
    except:
        print('Cannot load consolidated graphs')
        raise "cannot load consolidated graphs"
    for topic in graphs:
        index = 0
        for graph in graphs[topic]['graphs']:
            plt.figure(figsize=(6, 6))
            plt.title(f'{topic} network {index}')
            #plt.text(x=1, y=1, s=f'Positive Dyadicity: {graph["posDyadicity"]}')
            red_patch = mpatches.Patch(color='red', label=f'Negative towards {topic}')
            green_patch = mpatches.Patch(color='green', label=f'Positive towards {topic}')
            black_patch1 = mpatches.Patch(color='black', label=f'Pos Dyadicity {graph["posDyadicity"]}')
            black_patch2 = mpatches.Patch(color='black', label=f'Neg Dyadicity {graph["negDyadicity"]}')
            plt.legend(handles=[red_patch, green_patch, black_patch1, black_patch2])
            G, colorMap = getPlotableGraph(graph['graph'])
            nx.draw(G, node_color=colorMap, with_labels=False)
            plt.savefig(f'{ABSOLUTE_PLOT_FOLDER_PATH}{topic}_{index}.png')
            G.clear()
            plt.close()
            index += 1