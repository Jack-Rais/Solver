import tkinter as tk
from .mods import RectangleMode, CancelMode, OpenMode

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
            bg = color,
            highlightthickness = 0
        )
        
        self.canvas.place(
            x = int(self.root.winfo_width() * (1 - self.percent_width)),
            y = 0,
            height = int(self.root.winfo_height() * self.percent_height),
            width = int(self.root.winfo_width() * self.percent_width)
        )

        self.mode = RectangleMode()(self.canvas)

    
    def update_size(self, event:tk.Event = None):

        self.canvas.place(
            x = int(self.root.winfo_width() * (1 - self.percent_width)),
            height = int(self.root.winfo_height() * self.percent_height),
            width = int(self.root.winfo_width() * self.percent_width)
        )

    
    def change_mode(self, mode:str):

        self.mode.unbind()

        match mode:

            case "rectangle":
                self.mode = RectangleMode()(self.canvas, self.mode.nodes)

            case "cancel":
                self.mode = CancelMode()(self.canvas, self.mode.nodes)

            case "open":
                self.mode = OpenMode()(self.canvas, self.mode.nodes)