from ..bases import Edge, Node
from typing import Iterable


class ListEdges:

    def __init__(self, edges:list[Edge]| list[tuple] |  None = None):
        
        self.list_edges:list[Edge] = []
        
        if edges:
            for edge in edges:

                self.add_edge(
                    edge[0],
                    edge[1],
                    edge[2]
                )


    def add_edge(self, other_id:str, line_id:int, capacity:float = None) -> Edge:

        edge = Edge(other_id, line_id, capacity)
        self.list_edges.append(edge)

        return edge

    
    def get_line_by_id(self, id_tofind:str):

        return [edge.line_id for edge in self.list_edges if edge.other_id == id_tofind][0]
    

    def get_line_by_node(self, node_tofind:Node):
    
        return [edge.line_id for edge in self.list_edges if edge.other_id == node_tofind.id][0]
    
    def __repr__(self):
        
        to_add = "\n\t".join([edge.__repr__() for edge in self.list_edges])

        return "{\n\t" + to_add + '\n}'
    

    def __iter__(self) -> Iterable[Edge]:
        return iter(self.list_edges)