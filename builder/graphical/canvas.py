import tkinter as tk
from .modes.base_mode import Mode

from ..network import Network


class Canvas:


    def __init__(self, root: tk.Frame,
                       color: str = "lightgray",
                       modes: dict = None):
        
        self.root = root
        self.color = color

        self.modes = modes if modes else {}
        self.current_mode_name = None
        self.mode:Mode = None

        self.canvas = tk.Canvas(
            master = self.root,
            bg = self.color,
            highlightthickness = 0
        )
        self.canvas.place(
            x = 0,
            y = 0,
            width = int(self.root.winfo_width()),
            height = int(self.root.winfo_height())
        )

        self.canvas.bind('<Configure>', self.on_resize)


    def update_size(self, event: tk.Event = None):
        """Aggiorna la dimensione e il posizionamento del canvas."""

        self.canvas.place(
            width = int(self.root.winfo_width()),
            height = int(self.root.winfo_height())
        )

        self.height = int(self.canvas.winfo_height())
        self.width = int(self.canvas.winfo_width())

    
    def on_resize(self, event:tk.Event):

        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height

        self.height = int(event.height)
        self.width = int(event.width)

        self.canvas.scale("all", 0, 0, wscale, hscale)

        current_net = self.get_nodes()
        for node in current_net:

            startx, starty, endx, endy = self.canvas.coords(node.id)

            node.pos = (
                startx / self.canvas.winfo_width(),
                starty / self.canvas.winfo_height(),
                endx / self.canvas.winfo_width(),
                endy / self.canvas.winfo_height()
            )



    def change_mode(self, mode_name: str):
        """Cambia la modalità corrente."""

        if mode_name in self.modes:

            if self.mode:
                self.mode.unbind()

                self.current_mode_name = mode_name
                self.mode = self.modes[mode_name](**self.mode.pass_args())

            else:
                self.current_mode_name = mode_name
                self.mode = self.modes[mode_name](**{
                    "canvas": self.canvas,
                    "nodes": Network(),
                    "background": None
                })

            return True

        return False
    

    def get_nodes(self):
        """Restituisce i nodi attuali della modalità."""

        if self.mode:
            return self.mode.nodes
        
        return Network()


    def set_modes(self, modes: dict):
        """Configura le modalità disponibili per il canvas."""
        
        self.modes = modes
