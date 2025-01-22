import tkinter as tk
import networkx as nx

from .canvasVisual import CanvasVisualizer
from ...solver import Solver

class Simulator:

    def __init__(self, graph:nx.Graph, parent:tk.Tk):
        
        self.graph = graph
        self.solver = Solver(self.graph)
        self.canvas = CanvasVisualizer(parent, self.graph)
        

    def simulate(self, stat:str = 'units_count'):

        path = self.solver.solve()
        max_units = max([getattr(node[1]['node'], stat) for node in self.graph.nodes(data = True)])

        print(path)

    
    def set_graph(self, graph:nx.Graph):

        self.graph = graph
        self.solver = Solver(self.graph)
        self.canvas.set_graph(self.graph)

    def update_positions(self):
        
        pass