import tkinter as tk
from typing import Callable

class Button:

    button:tk.Canvas = None

    def update_size(self, master_width:int, master_height:int) -> None:
        pass


class RectangleButton(Button):

    def __init__(self, master:tk.Tk,
                       master_width:int,
                       master_height:int,
                       row:int = 0,
                       color:str = 'blue',
                       percent_padx:int | None = None,
                       percent_pady:int | None = None,
                       paddingx:int | None = None,
                       paddingy:int | None = None,
                       callback_func:Callable | None = None):
        
        self.paddingx = paddingx
        self.paddingy = paddingy

        self.percent_padx = percent_padx
        self.percent_pady = percent_pady
        self.row = row

        self.callback_func = callback_func if callback_func else lambda x: x

        self.button = tk.Canvas(
            master = master,
            bg = color,
            highlightthickness = 0
        )

        if paddingx is None:
            paddingx = (percent_padx if percent_padx else 0.1) * master_width

        if paddingy is None:
            paddingy = (percent_pady if percent_pady else 0.01) * master_height

        self.button.place(
            x = paddingx,
            y = int(master_height * 0.05) * row + paddingy * row + paddingy,
            height = int(master_height * 0.05),
            width = int(master_width * 0.9)
        )

        self.button.bind("<Button-1>", self.on_mouse_touch)


    def on_mouse_touch(self, event:tk.Event):
        
        self.callback_func('rectangle')


    def update_size(self, master_width:int, master_height:int) -> None:
        
        self.button.config(
            width = int(master_width * 0.8),
            height = int(master_height * 0.05)
        )

        if self.paddingx is None:
            paddingx = (self.percent_padx if self.percent_padx else 0.1) * master_width

        if self.paddingy is None:
            paddingy = (self.percent_pady if self.percent_pady else 0.01) * master_height
        
        self.button.place(
            x = paddingx,
            y = int(master_height * 0.05) * self.row + paddingy * self.row + paddingy,
            height = int(master_height * 0.05),
            width = int(master_width * 0.8)
        )


class CancelButton(Button):

    def __init__(self, master:tk.Tk,
                       master_width:int,
                       master_height:int,
                       row:int = 0,
                       color:str = 'blue',
                       percent_padx:int | None = None,
                       percent_pady:int | None = None,
                       paddingx:int | None = None,
                       paddingy:int | None = None,
                       callback_func:Callable | None = None ):
        
        self.paddingx = paddingx
        self.paddingy = paddingy

        self.percent_padx = percent_padx
        self.percent_pady = percent_pady
        self.row = row

        self.callback_func = callback_func if callback_func else lambda x: x

        self.button = tk.Canvas(
            master = master,
            bg = color,
            highlightthickness = 0
        )

        if paddingx is None:
            paddingx = (percent_padx if percent_padx else 0.1) * master_width

        if paddingy is None:
            paddingy = (percent_pady if percent_pady else 0.01) * master_height

        self.button.place(
            x = paddingx,
            y = int(master_height * 0.05) * row + paddingy * row + paddingy,
            height = int(master_height * 0.05),
            width = int(master_width * 0.9)
        )

        self.button.bind("<Button-1>", self.on_mouse_touch)

    def on_mouse_touch(self, event:tk.Event):
        
        self.callback_func('cancel')

    def update_size(self, master_width:int, master_height:int) -> None:
        
        self.button.config(
            width = int(master_width * 0.8),
            height = int(master_height * 0.05)
        )

        if self.paddingx is None:
            paddingx = (self.percent_padx if self.percent_padx else 0.1) * master_width

        if self.paddingy is None:
            paddingy = (self.percent_pady if self.percent_pady else 0.01) * master_height
        
        self.button.place(
            x = paddingx,
            y = int(master_height * 0.05) * self.row + paddingy * self.row + paddingy,
            height = int(master_height * 0.05),
            width = int(master_width * 0.8)
        )


class OpenButton(Button):

    def __init__(self, master:tk.Tk,
                       master_width:int,
                       master_height:int,
                       row:int = 0,
                       color:str = 'blue',
                       percent_padx:int | None = None,
                       percent_pady:int | None = None,
                       paddingx:int | None = None,
                       paddingy:int | None = None,
                       callback_func:Callable | None = None ):
        
        self.paddingx = paddingx
        self.paddingy = paddingy

        self.percent_padx = percent_padx
        self.percent_pady = percent_pady
        self.row = row

        self.callback_func = callback_func if callback_func else lambda x: x

        self.button = tk.Canvas(
            master = master,
            bg = color,
            highlightthickness = 0
        )

        if paddingx is None:
            paddingx = (percent_padx if percent_padx else 0.1) * master_width

        if paddingy is None:
            paddingy = (percent_pady if percent_pady else 0.01) * master_height

        self.button.place(
            x = paddingx,
            y = int(master_height * 0.05) * row + paddingy * row + paddingy,
            height = int(master_height * 0.05),
            width = int(master_width * 0.9)
        )

        self.button.bind("<Button-1>", self.on_mouse_touch)

    def on_mouse_touch(self, event:tk.Event):
        
        self.callback_func('open')

    def update_size(self, master_width:int, master_height:int) -> None:
        
        self.button.config(
            width = int(master_width * 0.8),
            height = int(master_height * 0.05)
        )

        if self.paddingx is None:
            paddingx = (self.percent_padx if self.percent_padx else 0.1) * master_width

        if self.paddingy is None:
            paddingy = (self.percent_pady if self.percent_pady else 0.01) * master_height
        
        self.button.place(
            x = paddingx,
            y = int(master_height * 0.05) * self.row + paddingy * self.row + paddingy,
            height = int(master_height * 0.05),
            width = int(master_width * 0.8)
        )