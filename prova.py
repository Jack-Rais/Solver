import networkx as nx
import matplotlib.pyplot as plt

from builder.graphical import Builder


root = Builder()
root.run()

### Problema con OpenMode 


nx.draw(
    root.nodes.graph,
    with_labels = True, 
    node_color = 'skyblue', 
    font_weight = 'bold',
    node_size = 2000
)

plt.show()