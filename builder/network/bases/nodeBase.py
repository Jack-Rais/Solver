from typing import Literal, Any

class Node:

    
    def __init__(self, id:str,
                       edges: Any = None,
                       capacity:float | None = None,
                       name:str | None = None,
                       type:Literal['node', 'safezone'] = 'node'):
        
        from ..lists import ListEdges
        
        self.id = id
        self.edges:ListEdges = edges
        self.capacity = capacity
        self.name = name
        self.type = type


    def set_id(self, new_id:str):
        self.id = new_id

    def add_edge(self, other_id:str, line_id:int, capacity:float = None):
        return self.edges.add_edge(other_id, line_id, capacity)
    
    def remove_edge(self, other_id:str):
        self.edges.remove_edge(other_id)