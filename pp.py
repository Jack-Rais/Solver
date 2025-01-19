import pickle
import matplotlib.pyplot as plt
import networkx as nx

with open('graph_saved.pkl', 'rb') as file:
    graph = pickle.load(file)

positions = dict()
for node in graph.nodes(data = True):

    print(node[1]['node'])

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
)

'''nx.draw(
    graph,
    with_labels = True, 
    node_color = 'skyblue', 
    font_weight = 'bold',
    node_size = 2000,
    pos = positions,

)'''

from system.solver import Solver

s = Solver(graph)
s.solve()

plt.show()