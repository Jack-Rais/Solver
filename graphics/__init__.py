import tkinter as tk

from .canvas import Canvas
from .button_bar import ButtonBar


class Builder:


    def __init__(self, width:int = 800, 
                       height:int = 600,
                       title:str = "Network") -> None:

        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(self.root, width, height)

        self.setup_widgets()


    def setup_widgets(self):

        self.button_bar = ButtonBar(
            self.root,
            callback_func = self.change_canvas_mode
        )

        self.canvas = Canvas(
            self.root
        )

        self.root.bind('<Configure>', self.update_size)

    @property
    def nodes(self):
        return self.canvas.mode.nodes

    def change_canvas_mode(self, mode:str):
        self.canvas.change_mode(mode)


    def update_size(self, event:tk.Event = None):

        self.canvas.update_size(event)
        self.button_bar.update_size(event)


    def center_app(self, root:tk.Tk, width:int, height:int) -> None:

        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{posx}+{posy}')
        root.update()

    def run(self):
        self.root.mainloop()