"""
graphs = {
    'topic1': {
        allGraphs = []
    },
    'topic2': {
        allGraphs = []
    }
}
"""

import sys
sys.path.insert(0, 'D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/data-collection/data')
from os import listdir
from os.path import isfile, join
import json

ABSOLUTE_DATA_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/data-collection/data"
ABSOLUTE_CONSOLIDATED_DATA_FOLDER_PATH = "D:/School/CollegeJunior/Fall2020/LING495/Project/repo/political-sentiment-graph/data-collection/consolidated_data"

def getAllFiles(path):
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]

def consolidateAllGraphs(files):
    singleStructure = {
        'trump': {
            'graphs': []
        },
        'biden': {
            'graphs': []
        }
    }
    for f in files:
        try:
            cacheFile = open(f)
            curGraph = json.load(cacheFile)
            if 'trump' in str(f):
                singleStructure['trump']['graphs'].append(curGraph)
            elif 'biden' in str(f):
                singleStructure['biden']['graphs'].append(curGraph)
            else:
                continue
        except:
            print(f'Could not open {f}')
    
    return singleStructure

def saveGraph(graph, title):
    print(f'Saving {title}')
    try:
        f = open(f'{ABSOLUTE_CONSOLIDATED_DATA_FOLDER_PATH}/{title}.json', 'w')
        f.write(json.dumps(graph))
        f.close()
        print(f'Saved {title}')
    except:
        print(f'Could not save {title}')

if __name__ == "__main__":
    files = getAllFiles(ABSOLUTE_DATA_FOLDER_PATH)
    graph = consolidateAllGraphs(files)
    saveGraph(graph, 'consolidated1')
