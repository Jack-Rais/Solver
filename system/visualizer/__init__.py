import tkinter as tk
import networkx as nx

from .canvasVisual import CanvasVisualizer


class Visualizer:

    def __init__(self, width:int = 600,
                       height:int = 500,
                       graph:nx.Graph | None = None,
                       title:str = "Visualizer"):
        
        self.graph = graph
        
        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(self.root, width, height)

        self.setup_widgets()
        if graph:
            self.set_graph(graph)

    
    def center_app(self, root: tk.Tk, width: int, height: int) -> None:

        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{posx}+{posy}')
        root.update()

    
    def set_graph(self, graph:nx.Graph):
        self.canvas.set_graph(graph)

    
    def setup_widgets(self):
        
        self.canvas = CanvasVisualizer(
            self.root,
            self.graph
        )
