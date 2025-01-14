import networkx as nx



class Solver:

    def __init__(self, data):
        self.graph = nx.Graph()

        self.update_data(data)

    
    def update_data(self, data):

        print(type(data))
        print(len(data))