from system.updater.updater import Updater
from system.visualizer import Visualizer
from builder import Builder
from system.solver.modifier import System
import pickle

import networkx as nx
import matplotlib.pyplot as plt

from copy import deepcopy
from system.solver.modifier import System


'''root = Builder()
root.run()

graph = root.nodes.graph'''

with open('graph_saved.pkl', 'rb') as file:
    graph:nx.Graph = pickle.load(file)

'''positions = dict()
for node in graph.nodes(data = True):

    #print(node[1]['node'])

    startx, starty, endx, endy = node[1]['node'].pos
    positions[node[0]] = (
        (startx + endx) / 2,
        1 - (starty + endy) / 2
    )
    
nx.draw_networkx(
    graph,
    with_labels = True, 
    node_color = 'skyblue', 
    font_weight = 'bold',
    node_size = 2000,
    pos = positions,
    labels = dict(
        (node[1]['node'].id, node[1]['node'].name) for node in graph.nodes(data = True)
    )
)
plt.show()'''


'''root = Builder()
root.run()'''

'''
for x in graph.nodes(data = True):
    print(x[1]['node'].id, x[1]['node'].units_count)'''

sis = System()

solver = Visualizer(graph = graph)
solver.run()













'''root = Updater(graph = graph)
root.run()'''