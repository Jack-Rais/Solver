import networkx as nx


class Solver:

    def __init__(self, graph:nx.Graph):

        self.graph = graph.to_directed()

    
    def solve(self):

        nodes_supply = [
            node[1]['node'] for node in self.graph.nodes(data = True) if node[1]['node'].capacity > 0
        ]
        nodes_demand = [
            node[1]['node'] for node in self.graph.nodes(data = True) if node[1]['node'].capacity < 0
        ]

        supply_total = sum([node.capacity for node in nodes_supply])
        demand_total = sum([])