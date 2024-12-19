import tkinter as tk
from graphics.canvas import Canvas


class Root:


    def __init__(self, width:int = 800, 
                       height:int = 600,
                       title:str = "Network") -> None:

        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(self.root, width, height)

        self.setup_widgets(self.root)


    def setup_widgets(self, root:tk.Tk):

        self.button_bar = tk.Frame(
            master = root,
            bg = 'blue',
            width = int(root.winfo_width() * 0.1),
            height = root.winfo_height()
        )

        self.button_bar.grid(
            row = 0,
            column = 0,
            sticky = 'ns'
        )

        self.canvas = Canvas(
            self.root
        )


    def center_app(self, root:tk.Tk, width:int, height:int) -> None:

        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{posx}+{posy}')
        root.update()


    def run(self):
        self.root.mainloop()


width, height = 600, 500

root = Root(
    width, height
)

root.run()