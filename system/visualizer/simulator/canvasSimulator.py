import tkinter as tk
import networkx as nx

from .canvasVisual import CanvasVisualizer
from ...solver import Solver

import matplotlib.pyplot as plt
import time


class Simulator:

    def __init__(self, graph:nx.Graph, parent:tk.Tk, stat:str = 'units_count'):
        
        self.graph = graph
        self.canvas:CanvasVisualizer = CanvasVisualizer(parent, self.graph)

        self.stat = stat
        self.set_graph(graph)


    def simulate(self):
        """
        Avvia il ciclo di aggiornamento usando il metodo after di tkinter.
        """

        total_path:tuple[float, dict[int, dict[int, int]]] = self.solver.solve()
        total_saved, self.path = total_path

        self.graph = self.solver.graph

        self.update_simulation()


    def update_simulation(self):
        """
        Esegue un passaggio della simulazione, aggiorna le posizioni e pianifica il prossimo aggiornamento.
        """

        path = self.prepare_path(self.path)
        self.update_positions(path)

        self.draw()

        # Pianifica il prossimo aggiornamento
        self.canvas.canvas.after(1000, self.update_simulation)

    
    def set_graph(self, graph: nx.Graph):

        self.graph = graph
        self.solver = Solver(self.graph)
        self.canvas.set_graph(self.graph)
        self.max_units = max(
            [
                node[1]['node'].capacity for node in self.graph.nodes(data=True) \
                    if node[1]['node'].type != 'safezone'
            ]
        )
        self.draw()

            

    def rgb_to_hex(self, r:int, g:int, b:int):
        return f"#{abs(r):02x}{abs(g):02x}{abs(b):02x}"

    
    def draw(self):

        for node in [node[1]['node'] for node in self.graph.nodes(data=True)]:

            if node.id not in ['super_supply', 'super_demand']:
                id_node = self.get_id_by_node(node)

                color = int(255 * (getattr(node, self.stat) / self.max_units))

                self.canvas.canvas.itemconfig(
                    id_node,
                    fill = self.rgb_to_hex(255 - color, 255 - color, 255 - color)
                )


    def prepare_path(self, path:dict[int, dict[int, float]]):

        new_path = dict()
        for node_id, nodes_to in path.items():

            if node_id not in ['super_supply', 'super_demand']:
                node = self.graph.nodes[node_id]['node']

                if getattr(node, self.stat) > 0:
                    new_path[node_id] = {
                        other_id: min(
                            flow, getattr(node, self.stat), self.graph[node_id][other_id]['edge'].capacity
                        ) for other_id, flow in nodes_to.items()
                    }

        cleaned_path = dict()
        for node_id, nodes_to in new_path.items():

            for other_id, flow in nodes_to.items():
                
                if flow != 0:
                
                    if cleaned_path.get(node_id, None) is None:
                        cleaned_path[node_id] = {
                            other_id: flow
                        }

                    else:
                        cleaned_path[node_id][other_id] = flow

        return cleaned_path
    


    def update_positions(self, path: dict[str, dict]):
        """
        Aggiorna le posizioni dei nodi in base al percorso e al flusso calcolato.
        Restituisce un dizionario con le unità rimanenti per ogni nodo.
        """

        for id_room, to_rooms in path.items():
            current_node = self.graph.nodes[id_room]['node']  # Nodo sorgente

            for target_id, flow in to_rooms.items():
                target_node = self.graph.nodes[target_id]['node']

                print(f"From {current_node.id} ({current_node.units_count}) ", end='')
                print(f"to {target_node.id} ({target_node.units_count}) ", end='')
                print(f"{flow} units")

                current_node.units_count -= flow
                target_node.units_count += flow

        print('-' * 40)

    def get_id_by_node(self, node):
        return self.canvas.get_id_by_node(node)