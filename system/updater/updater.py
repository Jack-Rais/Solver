import tkinter as tk
import networkx as nx

from functools import partial
from ..visualizer.simulator.canvasSimulator import Simulator

import os 
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join('...'), project_root)

from builder.graphical.utils.pop_up import Popup


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

        for node in graph.nodes(data = True):
            node[1]['node'].units_count = 0

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
            text = "Start"
        )
        add_button.grid(
            row=1,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )

        add_button = tk.Button(
            frame
        )
        start_button.config(
            command = partial(self.change_mode, 'sub'),
            bg = 'green',
            text = "Start"
        )
        start_button.grid(
            row=2,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )


    def change_mode(self, mode:str):

        match mode:

            case 'sim':
                
                self.canvas.canvas.canvas.destroy()
                self.canvas = Simulator(self.graph, self.root)
                self.canvas.simulate()

            case 'add':

                self.canvas = 

            case 'sub':

                self.canvas = 



    
    def run(self):
        self.root.mainloop()