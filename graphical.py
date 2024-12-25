import networkx as nx
import matplotlib.pyplot as plt

from graphics import Builder
from network.network import Nodes


root = Builder()
root.run()

graph = Nodes(root.nodes)

nx.draw(graph.nodes)
plt.show()