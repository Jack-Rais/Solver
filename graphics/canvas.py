import tkinter as tk
from .mods import RectangleMode

class Canvas:

    def __init__(self, root: tk.Tk,
                       percent_width:float = 0.9,
                       percent_height:float = 1,
                       color:str = "lightgray"):
        
        self.root = root
        self.percent_width = percent_width
        self.percent_height = percent_height

        self.canvas = tk.Canvas(
            master = self.root,
            height = int(self.root.winfo_height() * self.percent_height),
            width = int(self.root.winfo_width() * self.percent_width),
            bg = color
        )
        
        self.canvas.grid(
            row = 0, 
            column = 1, 
            sticky = 'ns'
        )

        self.mode = RectangleMode()(self.canvas)

    
    def update_size(self, event:tk.Event = None):

        self.canvas.config(
            height = int(self.root.winfo_height() * self.percent_height),
            width = int(self.root.winfo_width() * self.percent_width)
        )

        self.canvas.place(
            x = int(self.root.winfo_width() * (1 - self.percent_width))
        )