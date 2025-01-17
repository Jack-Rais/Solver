import networkx as nx
import matplotlib.pyplot as plt

from builder.graphical import Builder
from builder.network.network import Network


root = Builder()
root.run()

net = Network()
net.fit(root.nodes)


nx.draw(
    net.graph,
    with_labels = True, 
    node_color = 'skyblue', 
    font_weight = 'bold',
    node_size = 2000
)

plt.show()