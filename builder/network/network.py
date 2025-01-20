import networkx as nx
import pickle

from .bases import Node, Edge
from .lists import ListNodes, ListEdges

from typing import Iterable

class Network:


    def __init__(self):
        self.graph = nx.Graph()

    
    def add_node(self, node_id:str, **attrs):

        if len(attrs) != 1:

            node_new = Node(
                node_id,
                ListEdges(attrs.get('edges')),
                attrs.get('units_count'),
                attrs.get('capacity'),
                attrs.get('name'),
                attrs.get('type'),
                attrs.get('position')
            )

        else:

            node_new = attrs['node']
        
        self.graph.add_node(
            node_id,
            node = node_new
        )

        return node_new

    
    def search_node(self, id_tofind:str) -> Node:

        return self.graph.nodes[id_tofind]['node']

    
    def add_edge(self, id_self:str, 
                       other_id:str, 
                       line_id:int, 
                       capacity:float):

        node:Node = self.search_node(id_self)

        edge = node.add_edge(other_id, line_id, capacity)

        x = self.graph.add_edge(
            id_self, other_id,
            edge = edge
        )

    
    def get_node(self, id:str) -> Node:

        return self.graph.nodes(data = True)[id]['node']
    

    def remove(self, to_remove: Node | str):
        
        if isinstance(to_remove, str):
            self.graph.remove_node(to_remove)

        elif isinstance(to_remove, Node):
            self.graph.remove_node(to_remove.id)

        else:
            raise ValueError(f"The input {to_remove} is not in the correct form")
    
    def __iter__(self) -> Iterable[Node]:
        return iter([node[1]['node'] for node in self.graph.nodes(data = True)])
    

    def save(self, filepath:str = 'graph_saved.pkl'):

        with open(filepath, 'wb') as file:
            pickle.dump(self.graph, file)