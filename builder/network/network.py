import networkx as nx

from .bases import Node, Edge
from .lists import ListNodes, ListEdges

class Network:


    def __init__(self):
        self.graph = nx.Graph()

    
    def add_node(self, node_id:str, char: str | None = None, **attrs):

        if len(attrs) != 1:

            node_new = Node(
                attrs[char],
                ListEdges(attrs.get('edges', None)),
                attrs.get('capacity', None),
                attrs.get('name', None),
                attrs.get('type', None),
            )

        else:

            node_new = attrs['node']
        
        self.graph.add_node(
            node_id,
            node = node_new
        )

    
    def search_node(self, id_tofind:str):

        return self.graph.nodes[id_tofind]['node']

    
    def add_edge(self, id_self:str, 
                       other_id:str, 
                       line_id:int, 
                       capacity:float):

        node:Node = self.search_node(id_self)
        edge = node.add_edge(other_id, line_id, capacity)

        self.graph.add_edge(
            id_self, other_id,
            node = edge
        )

    
    def fit(self, data:list[dict], char:str = 'id'):

        for node in data:

            id_node = node.pop(char)

            node_new = Node(
                id_node,
                ListEdges(node.get('edges', None)),
                node.get('capacity', None),
                node.get('name', None),
                node.get('type', None),
            )
            
            self.add_node(
                id_node,
                char = char,
                node = node_new
            )

            for edge in ListEdges(node.get('edges')):
                self.add_edge(
                    id_node,
                    edge.other_id,
                    edge.line_id,
                    edge.capacity
                )
        