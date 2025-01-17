

class Edge:

    def __init__(self, other_id:str, 
                       line_id:int,
                       capacity:float = None):
        
        self.other_id = other_id 
        self.line_id = line_id
        self.capacity = capacity

    
    def id_equal(self, id_comparison:str):
        return id_comparison == self.other_id
    

    def __getitem__(self, name):
        
        if isinstance(name, int):

            match name:

                case 0:
                    return self.other_id
                
                case 1:
                    return self.line_id
                
                case 2:
                    return self.capacity
        
        elif isinstance(name, str):

            match name:

                case 'other_id':
                    return self.other_id
                
                case 'line_id':
                    return self.line_id
                
                case 'capacty':
                    return self.capacity
        
        raise ValueError(f'Index: {name} not in Edge')
    

    def __repr__(self):
        return f"Other id: {self.other_id}, Line id: {self.line_id}, Capacity: {self.capacity}"