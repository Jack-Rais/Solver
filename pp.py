import pickle
import matplotlib.pyplot as plt
import networkx as nx

'''
1, {
        Other id: 3, Line id: 6, Capacity: 56.0
        Other id: 2, Line id: 9, Capacity: 67.0
}, 12, 12, node, (0.2537037037037037, 0.15, 0.40185185185185185, 0.366)
2, {
        Other id: 4, Line id: 8, Capacity: 67.0
        Other id: 1, Line id: 9, Capacity: 67.0
        Other id: 5, Line id: 10, Capacity: 67.0
}, 23, 23, node, (0.40185185185185185, 0.1, 0.5407407407407407, 0.488)
3, {
        Other id: 1, Line id: 6, Capacity: 56.0
        Other id: 4, Line id: 7, Capacity: 67.0
}, 34, 34, node, (0.20185185185185187, 0.366, 0.40185185185185185, 0.598)
4, {
        Other id: 3, Line id: 7, Capacity: 67.0
        Other id: 2, Line id: 8, Capacity: 67.0
}, 45, 45, node, (0.40185185185185185, 0.488, 0.6, 0.72)
5, {
        Other id: 2, Line id: 10, Capacity: 67.0
        Other id: 11, Line id: 12, Capacity: 34
}, 56, 56, node, (0.5407407407407407, 0.17, 0.6925925925925925, 0.512)
11, {
        Other id: 5, Line id: 12, Capacity: 34
}, -34, None, safezone, (0.7925925925925926, 0.282, 0.8481481481481481, 0.342)

'''
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

plt.show()