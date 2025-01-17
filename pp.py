'''from builder.network.lists import ListEdges

l = ListEdges(
    [(1, 2, 3), (1, 2, 3), (1, 2, 3)]
)

print(l)'''

import networkx as nx


graph = nx.Graph()
graph.add_node(
    '01',
    node = 'pippocaio'
)

graph.add_node(
    '02',
    node = 'pippopippo'
)

print(graph.nodes['01'])