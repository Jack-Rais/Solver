import networkx as nx
import pickle

from system.solver.modifier import System
from system.solver import Solver

import matplotlib.pyplot as plt


with open('graph_saved.pkl', 'rb') as file:
    graph:nx.Graph = pickle.load(file)


positions = dict()
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
    node_size = 200,
    pos = positions,
    labels = dict(
        (node[1]['node'].id, node[1]['node'].id) for node in graph.nodes(data = True)
    )
)
plt.show()


sys = System()
graph = sys.normalize_v1_graph(graph)

p = Solver(graph).solve_every_room(graph)
print(p)


positions = dict()
for node in graph.nodes(data = True):

    print(node[1])
    positions[node[0]] = node[1]['center']
    
nx.draw_networkx(
    graph,
    with_labels = True, 
    node_color = 'skyblue', 
    font_weight = 'bold',
    node_size = 200,
    pos = positions,
    #labels = dict(
    #    (node[1]['node'].id, node[1]['node'].name) for node in graph.nodes(data = True)
    #)
)
plt.show()