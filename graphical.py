import tkinter as tk
from graphics.canvas import Canvas
from graphics.button_bar import ButtonBar


class Root:


    def __init__(self, width:int = 800, 
                       height:int = 600,
                       title:str = "Network") -> None:

        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(self.root, width, height)

        self.setup_widgets(self.root)


    def setup_widgets(self, root:tk.Tk):

        self.button_bar = ButtonBar(
            self.root,
            callback_func = self.change_canvas_mode
        )

        self.canvas = Canvas(
            self.root
        )

        self.root.bind('<Configure>', self.update_size)
        self.root.bind('<Button-1>', self.pos)

    def pos(self, event):
        print(event.x, event.y)
        
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

    
    ## Aggiungere 


    def run(self):
        self.root.mainloop()


width, height = 600, 500

root = Root(
    width, height
)

root.run()