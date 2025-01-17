from typing import Literal

class Node:

    
    def __init__(self, id:str,
                       edges:list | None = None,
                       capacity:float | None = None,
                       name:str | None = None,
                       type:Literal['node', 'safezone'] = 'node'):
        
        self.id = id
        self.edges = edges
        self.capacity = capacity
        self.name = name
        self.type = type


    def set_id(self, new_id:str):
        self.id = new_id

    def add_edge(self, other_id:str, line_id:int, capacity:float = None):
        return self.edges.add_edge(other_id, line_id, capacity)


    def __repr__(self):

        pass