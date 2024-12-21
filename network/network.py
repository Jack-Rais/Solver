import networkx as nx


class Nodes:


    def __init__(self):
        self.nodes = nx.Graph()


    def add_node(self, node_id:str, **kwargs):

        self.nodes.add_node(
            node_id,
            **kwargs
        )


    def connect_nodes(self, node1_id:str, node2_id:str, **kwargs):

        self.nodes.add_edge(
            node1_id,
            node2_id,
            **kwargs
        )

    
    def remove_node(self, node_id:str):

        self.nodes.remove_node(node_id)

    
    def remove_connection(self, node1_id:str, node2_id:str):

        self.nodes.remove_edge(node1_id, node2_id)