import tkinter as tk


class Canvas:


    def __init__(self, root: tk.Frame,
                       color: str = "lightgray",
                       modes: dict = None):
        
        self.root = root
        self.color = color

        self.modes = modes if modes else {}
        self.current_mode_name = None
        self.mode = None

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


    def update_size(self, event: tk.Event = None):
        """Aggiorna la dimensione e il posizionamento del canvas."""

        self.canvas.place(
            width = int(self.root.winfo_width()),
            height = int(self.root.winfo_height())
        )


    def change_mode(self, mode_name: str):
        """Cambia la modalità corrente."""

        if mode_name in self.modes:

            if self.mode:
                self.mode.unbind()

                self.current_mode_name = mode_name
                self.mode = self.modes[mode_name](self.canvas, self.mode.nodes)

            else:
                self.current_mode_name = mode_name
                self.mode = self.modes[mode_name](self.canvas, self.mode)

            return True

        return False
    

    def get_nodes(self):
        """Restituisce i nodi attuali della modalità."""

        if self.mode:
            return self.mode.nodes
        
        return []


    def set_modes(self, modes: dict):
        """Configura le modalità disponibili per il canvas."""
        
        self.modes = modes
