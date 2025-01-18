import networkx as nx
import matplotlib.pyplot as plt

from builder import Builder


root = Builder()
root.run()

positions = dict()
for node in root.nodes.graph.nodes(data = True):

    print(node[1]['node'])

    startx, starty, endx, endy = node[1]['node'].pos
    positions[node[0]] = (
        (startx + endx) / 2,
        1 - (starty + endy) / 2
    )

nx.draw(
    root.nodes.graph,
    with_labels = True, 
    node_color = 'skyblue', 
    font_weight = 'bold',
    node_size = 2000,
    pos = positions
)

root.save()

plt.show()