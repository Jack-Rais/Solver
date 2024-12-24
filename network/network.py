import networkx as nx


class Nodes:


    def __init__(self, data = None):
        self.nodes = nx.Graph()

        if data:
            self.wrap(data)

    def wrap(self, data:list[dict]):

        for node in data:
            self.nodes.add_node(node['id'])

            for edge in node['edges']:
                self.nodes.add_edge(node['id'], edge[0])

