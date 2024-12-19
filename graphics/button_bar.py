import tkinter as tk


class ButtonBar:

    def __init__(self, root:tk.Tk,
                       percent_width:float = 0.1,
                       percent_height:float = 1,
                       color:str = 'gray'):

        self.root = root
        self.percent_width = percent_width
        self.percent_height = percent_height

        self.button_bar = tk.Frame(
            master = root,
            width = int(self.root.winfo_width() * self.percent_width),
            height = int(self.root.winfo_height() * self.percent_height),
            bg = color
        )

        self.button_bar.grid(
            row = 0,
            column = 0,
            sticky = 'ns'
        )

    
    def update_size(self, event:tk.Event = None):

        self.button_bar.config(
            height = int(self.root.winfo_height() * self.percent_height),
            width = int(self.root.winfo_width() * self.percent_width)
        )