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


    
    def __get_room_path(self, graph, nodes_supply, nodes_demand):

        for node in nodes_supply:

            path_final = None
            min_val_path = None

            nodes_to_iter = [
                node_it for node_it in nodes_demand if abs(node_it[1]['units_count']) > abs(node[1]['units_count'])
            ]
            
            for node_arrive in nodes_to_iter:

                path_len = nx.shortest_path_length(
                    graph,
                    node[0], 
                    node_arrive[0],
                    'weight'
                )


                if min_val_path == None:

                    min_val_path = path_len

                    path = nx.shortest_path(
                        graph,
                        node[0], 
                        node_arrive[0],
                        'weight'
                    )

                    if path is not None:
                        path_final = path

                
                elif min_val_path > path_len:

                    min_val_path = path_len

                    path = nx.shortest_path(
                        graph,
                        node[0], 
                        node_arrive[0],
                        'weight'
                    )

                    if path is not None:
                        path_final = path

        return path_final
    

    def solve_every_room(self, graph:nx.Graph):

        nodes_supply = [
            node for node in graph.nodes(data = True) if node[1]['units_count'] > 0
        ]
        nodes_demand = [
            node for node in graph.nodes(data = True) if node[1]['units_count'] < 0
        ]


        dict_paths = dict()


        while len(nodes_supply) > 0:

            
            path_final = self.__get_room_path(
                graph,
                nodes_supply,
                nodes_demand
            )

            if path_final is None:
                return False, dict_paths, {
                    node[0]: node[1]['center'] for node in graph.nodes(data = True)
                }
        

            try:

                start_node = graph.nodes[path_final[0]]

                nodes_supply.remove((path_final[0], start_node))
                dict_paths[path_final[0]] = path_final

                end_node = graph.nodes[path_final[-1]]

                nx.set_node_attributes(
                    graph, 
                    {
                        path_final[-1]: {
                            'units_count': end_node['units_count'] + start_node['units_count']
                        }
                    }
                )

                nodes_supply = [(node[0], graph.nodes[node[0]]) for node in nodes_supply]
                nodes_demand = [(node[0], graph.nodes[node[0]]) for node in nodes_demand]

            except TypeError:
                return False, dict_paths, {
                    node[0]: node[1]['center'] for node in graph.nodes(data = True)
                }
            
        return True, dict_paths, {
            node[0]: node[1]['center'] for node in graph.nodes(data = True)
        }
    

    def clean_path(self, path:dict[int, list[str]]):

        dict_result = dict()

        for idx, lista_path in path.items():
            lista_final = []

            for elem in lista_path:

                res = elem.split('-')
                if len(res) == 1:

                    if not res[0] in lista_final:
                        lista_final.append(res[0])

                else:

                    if not res[0] in lista_final:
                        lista_final.append(res[0])

                    if not res[1] in lista_final:
                        lista_final.append(res[1])

            dict_result[idx] = lista_final


        return dict_result


    def clean_path_points(self, path:dict[int, list[str]], pos:dict[str, tuple[int, int]]):

        result_dict = dict()

        for idx, path_intern in tuple(path.items()):
            path_final = [pos[path_intern[0]]]
            
            for n, elem in enumerate(path_intern):
                
                if "-" in elem:
                    path_final.append(pos[elem])

            path_final.append(pos[path_intern[-1]])



            result_dict[idx] = path_final

        return result_dict