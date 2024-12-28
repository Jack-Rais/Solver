import networkx as nx
import matplotlib.pyplot as plt

from graphics import Builder
from network.network import Nodes


root = Builder()
root.run()

print(root.nodes)

graph = Nodes(root.nodes)

print(graph.nodes)

nx.draw(graph.nodes)

print()
for node in graph.nodes.nodes(data = True):
    print(node)
print()

print()
for node in graph.nodes.edges(data = True):
    print(node)
print()

print(nx.dijkstra_path(graph.nodes, '0', '2'))
plt.show()