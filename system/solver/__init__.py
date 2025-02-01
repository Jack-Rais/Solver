import networkx as nx

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, '...'))

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from builder.network.bases import Node, Edge
from builder.network.lists import ListEdges

import matplotlib.pyplot as plt


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

        print(nodes_supply)
        print(nodes_demand)

        for u, v, data in self.graph.edges(data = True):

            self.graph[u][v]['capacity'] = float('inf')
        

        for node in nodes_supply:

            for edge in node.edges:
                edge.capacity = node.units_count
                self.graph[node.id][edge.other_id]['capacity'] = node.units_count

        for node in nodes_demand:

            for edge in node.edges:
                edge.capacity = node.units_count
                self.graph[node.id][edge.other_id]['capacity'] = node.units_count

        supply_total = sum([node.units_count for node in nodes_supply])
        demand_total = sum([abs(node.units_count) for node in nodes_demand])

        super_supply = Node(
            'super_supply',
            ListEdges([
                Edge(node.id, None, abs(node.units_count)) for node in nodes_supply 
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
                Edge(node.id, None, abs(node.units_count)) for node in nodes_demand 
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

        for v in nodes_supply:
            self.graph.add_edge(
                super_supply.id, 
                v.id, 
                edge = Edge(v, None, v.units_count),
                capacity = abs(v.units_count)
            )

        self.graph.add_node(
            super_demand.id,
            node = super_demand
        )

        for v in nodes_demand:
            self.graph.add_edge(
                v.id, 
                super_demand.id, 
                edge = Edge(v, None, v.units_count),
                capacity = abs(v.units_count)
            )
        
        shortest = nx.maximum_flow(
            self.graph,
            super_supply.id,
            super_demand.id
        )

        return shortest

