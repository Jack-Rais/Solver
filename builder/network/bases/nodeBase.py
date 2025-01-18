from typing import Literal, Any

class Node:

    
    def __init__(self, id:str,
                       edges: Any,
                       capacity:float | None,
                       name:str | None,
                       type:Literal['node', 'safezone'],
                       position:tuple | None):
        
        from ..lists import ListEdges
        
        self.id = id
        self.edges:ListEdges = edges
        self.capacity = capacity
        self.name = name
        self.type = type
        self.pos = position


    def set_id(self, new_id:str):
        self.id = new_id

    def add_edge(self, other_id:str, line_id:int, capacity:float = None):
        return self.edges.add_edge(other_id, line_id, capacity)
    
    def remove_edge(self, other_id:str):
        self.edges.remove_edge(other_id)

    def __repr__(self):
        return f"{self.id}, {self.edges}, {self.capacity}, {self.name}, {self.type}, {self.pos}"