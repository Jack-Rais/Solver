import tkinter as tk
import networkx as nx

#import sys
#import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functools import partial
from ..visualizer.simulator.canvasSimulator import Simulator
from .modes.AddMode import AddMode
from .modes.SubMode import SubMode


class Updater:

    def __init__(self, width:int = 600,
                       height:int = 500,
                       graph:nx.Graph | None = None,
                       title:str = "Updater"):
        
        self.graph = graph
        
        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(width, height)

        self.setup_widgets()
        if graph:
            self.set_graph(graph)

    
    def center_app(self, width: int, height: int) -> None:

        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        self.root.geometry(f'{width}x{height}+{posx}+{posy}')
        self.root.update()

    
    def set_graph(self, graph:nx.Graph):

        self.max_units = 0
        for node in graph.nodes(data = True):

            if node[1]['node'].units_count > self.max_units:
                self.max_units = node[1]['node'].units_count

            node[1]['node'].units_count = 0

        self.nodes = [(node[1]['node'], node[1]['node'].id) for node in graph.nodes(data = True)]
        self.canvas.set_graph(graph)

    
    def setup_widgets(self):

        leftframe = tk.Frame(self.root, bg='lightgray', border=2)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=9)
        self.root.grid_rowconfigure(0, weight=1)

        leftframe.grid(column=0, row=0, sticky="nsew", padx=2, pady=2)
        
        self.canvas = Simulator(
            self.graph,
            self.root
        )

        self.setup_buttons(leftframe)
    
    def setup_buttons(self, frame:tk.Frame):

        frame.grid_columnconfigure(0, weight = 1)

        start_button = tk.Button(
            frame
        )
        start_button.config(
            command = partial(self.change_mode, 'sim'),
            bg = 'green',
            text = "Start"
        )
        start_button.grid(
            row = 0,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )

        add_button = tk.Button(
            frame
        )
        add_button.config(
            command = partial(self.change_mode, 'add'),
            bg = 'green',
            text = "Add"
        )
        add_button.grid(
            row=1,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )

        sub_button = tk.Button(
            frame
        )
        sub_button.config(
            command = partial(self.change_mode, 'sub'),
            bg = 'green',
            text = "Sub"
        )
        sub_button.grid(
            row=2,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )


    def change_mode(self, mode:str):

        self.canvas.unbind()

        match mode:

            case 'sim':
                
                self.canvas = Simulator(self.graph, self.root)
                self.canvas.simulate()

            case 'add':
                
                if isinstance(self.canvas, Simulator):
                    self.nodes = self.canvas.canvas_intern.nodes

                self.canvas = AddMode(
                    self.canvas.canvas, 
                    self.graph, 
                    self.max_units, 
                    self.nodes
                )

            case 'sub':

                if isinstance(self.canvas, Simulator):
                    self.nodes = self.canvas.canvas_intern.nodes

                self.canvas = SubMode(
                    self.canvas.canvas, 
                    self.graph, 
                    self.max_units, 
                    self.nodes
                )
    
    def run(self):
        self.root.mainloop()