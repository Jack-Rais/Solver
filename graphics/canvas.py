import tkinter as tk

class Canvas:

    def __init__(self, root: tk.Tk,
                       percent_width:float = 0.9,
                       percent_height:float = 1):
        
        self.root = root

        self.canvas = tk.Canvas(
            master = self.root,
            width = int(self.root.winfo_width() * percent_width),
            bg = 'red'
        )
        
        self.canvas.grid(
            row = 0, 
            column = 1, 
            sticky = 'ns'
        )
