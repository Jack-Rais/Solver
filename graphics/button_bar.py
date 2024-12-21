import tkinter as tk

from .buttons import RectangleButton, Button, CancelButton

from functools import partial
from typing import Callable


class ButtonBar:

    def __init__(self, root:tk.Tk,
                       percent_width:float = 0.2,
                       percent_height:float = 1,
                       color:str = 'gray',
                       callback_func: Callable | None = None):

        self.root = root
        self.percent_width = percent_width
        self.percent_height = percent_height

        self.callback_func = callback_func
        self.buttons:list[Button] = []

        self.button_bar = tk.Frame(
            master = root,
            width = int(self.root.winfo_width() * self.percent_width),
            height = int(self.root.winfo_height() * self.percent_height),
            bg = color
        )

        self.button_bar.place(
            x = 0, 
            y = 0,
            width = int(self.root.winfo_width() * self.percent_width),
            height = int(self.root.winfo_height() * self.percent_height)
        )

        self.add_buttons()

    def add_buttons(self):

        bar_width = int(self.root.winfo_width() * 0.1)
        bar_height = int(self.root.winfo_width() * 1)

        button1 = RectangleButton(
            self.button_bar,
            bar_width, 
            bar_height,
            color = 'blue',
            callback_func = self.callback_func
        )

        button2 = CancelButton(
            self.button_bar,
            bar_width, 
            bar_height,
            color = 'red',
            row = 2,
            callback_func = self.callback_func
        )

        self.buttons.extend([button1, button2])


    
    def update_size(self, event:tk.Event = None):

        new_height = int(self.root.winfo_height() * self.percent_height)
        new_width = int(self.root.winfo_width() * self.percent_width)

        self.button_bar.place(
            height = new_height,
            width = new_width
        )

        for button in self.buttons:
            button.update_size(new_width, new_height)

        