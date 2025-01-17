from ..bases import Node
from . import ListEdges

class ListNodes:

    def __init__(self):
        
        self.nodes:list[Node] = []

    
    def get_node(self, id_node):

        for node in self.nodes:
            if node.id == id_node:
                return node