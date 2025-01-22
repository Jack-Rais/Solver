import networkx as nx

import sys
import os

# Add the project root to the system path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, '...'))



from builder.network.bases import Node, Edge
from builder.network.lists import ListEdges

class Solver:

    def __init__(self, graph:nx.Graph):

        self.graph = graph.to_directed()

    
    def solve(self):

        nodes_supply = [
            node[1]['node'] for node in self.graph.nodes(data = True) if node[1]['node'].units_count > 0
        ]
        nodes_demand = [
            node[1]['node'] for node in self.graph.nodes(data = True) if node[1]['node'].units_count < 0
        ]

        supply_total = sum([node.units_count for node in nodes_supply])
        demand_total = sum([abs(node.units_count) for node in nodes_demand])

        super_supply = Node(
            'super_supply',
            ListEdges([
                Edge(node.id, None, supply_total) for node in nodes_supply 
            ]),
            supply_total,
            supply_total,
            'super_supply',
            'node',
            (0, 0, 0, 0)
        )

        super_demand = Node(
            'super_demand',
            ListEdges([
                Edge(node.id, None, demand_total) for node in nodes_demand 
            ]),
            -demand_total,
            -demand_total,
            'super_supply',
            'node',
            (0, 0, 0, 0)
        )

        self.graph.add_node(
            super_supply.id,
            node = super_supply
        )

        for v in [node.id for node in nodes_supply]:
            self.graph.add_edge(super_supply.id, v, edge = Edge(v, None, supply_total))

        self.graph.add_node(
            super_demand.id,
            node = super_demand
        )

        for v in [node.id for node in nodes_demand]:
            self.graph.add_edge(v, super_demand.id, edge = Edge(v, None, demand_total))

        
        def weight_function(u, v, data):
            return data['edge'].capacity
        
        import matplotlib.pyplot as plt

        nx.draw_networkx(
            self.graph,
            with_labels = True, 
            node_color = 'skyblue', 
            font_weight = 'bold',
            node_size = 2000,
            labels = dict(
                (node[1]['node'].id, node[1]['node'].id) for node in self.graph.nodes(data = True)
            )
        )

        plt.show()

        for u, v, data in self.graph.edges(data = True):
            
            self.graph[u][v]['capacity'] = data['edge'].capacity
        
        shortest = nx.maximum_flow(
            self.graph,
            super_supply.id,
            super_demand.id
        )

        return shortest

