import tkinter as tk
from graphics.canvas import Canvas  

class Root:

    def __init__(self, width: int = 800,
                       height: int = 600,
                       title: str = "Network") -> None:

        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(self.root, width, height)

        self.setup_widgets()

        print('--', self.canvas.canvas.winfo_width())
        print('--', self.canvas.canvas.winfo_height())

    def setup_widgets(self):
        
        self.root.update()
        print('cao', self.root.winfo_width())

        self.button_bar = tk.Frame(
            master = self.root,
            bg = 'blue',
            width = int(self.root.winfo_width() * 0.1),
            height = self.root.winfo_height()
        )
        self.button_bar.grid(
            row = 0, 
            column = 0, 
            sticky = 'ns'
        )

        self.canvas = Canvas(
            self.root
        )

        print(self.canvas.canvas.winfo_width())
        print(self.canvas.canvas.winfo_height())

        # Configura la griglia per l'espansione
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def center_app(self, root: tk.Tk, width: int, height: int) -> None:
        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{posx}+{posy}')

    def run(self):
        self.root.mainloop()


# Esegui l'app
width, height = 600, 500

root = Root(width, height)
root.run()
