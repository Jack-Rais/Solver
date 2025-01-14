import tkinter as tk
from .canvas import Canvas
from .button_bar import ButtonBar

from .modes import RectangleMode, CancelMode, OpenMode, SafeZoneMode, BackgroundFile


class Builder:


    def __init__(self, width: int = 600, 
                       height: int = 500, 
                       title: str = "Network") -> None:

        self.root = tk.Tk()
        self.root.title(title)
        self.center_app(self.root, width, height)

        self.current_floor = 0
        self.floors: dict[int, Canvas] = {}

        self.setup_widgets()


    def setup_widgets(self):

        self.button_bar = ButtonBar(
            self.root,
            callback_func=self.change_canvas_mode
        )

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side="right", fill="both", expand=True)

        self.add_floor()

        self.root.bind('<Configure>', self.update_size)


    @property
    def nodes(self):
        return self.floors[self.current_floor].mode.nodes


    def change_canvas_mode(self, mode: str):
        self.floors[self.current_floor].change_mode(mode)
        
        ### Inserire la logica per cambiare piano creare il bottone per farlo


    def update_size(self, event: tk.Event = None):

        if self.current_floor in self.floors:
            self.floors[self.current_floor].update_size(event)

        self.button_bar.update_size(event)


    def center_app(self, root: tk.Tk, width: int, height: int) -> None:

        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{posx}+{posy}')
        root.update()

    def add_floor(self):
        # Calcola il numero del nuovo piano
        floor_number = len(self.floors)
        
        # Crea un nuovo Canvas configurato
        new_canvas = Canvas(
            root = self.canvas_frame,
            modes = {
                "rectangle": RectangleMode,
                "cancel": CancelMode,
                "open": OpenMode,
                "safezone": SafeZoneMode,
                "filebackground": BackgroundFile
            },
            color = "lightgray"
        )
        
        # Aggiunge il canvas al dizionario dei piani
        self.floors[floor_number] = new_canvas
        
        # Passa automaticamente al nuovo piano
        self.switch_floor(floor_number)


    def switch_floor(self, floor_number: int):

        if floor_number in self.floors:

            for canvas in self.floors.values():
                canvas.canvas.pack_forget()
                

            self.floors[floor_number].canvas.pack(fill="both", expand=True)
            self.current_floor = floor_number

        else:
            print(f"Piano {floor_number} non trovato!")


    def run(self):
        self.root.mainloop()
