import tkinter as tk

from .buttons import Button, \
                        RectangleButton, \
                            CancelButton, \
                                OpenButton, \
                                    SafeZoneButton, \
                                        FileBackground

from typing import Callable, Optional


class ButtonBar:

    def __init__(self, root: tk.Tk,
                       percent_width: float = 0.1,
                       percent_height: float = 1,
                       color: str = 'gray',
                       callback_func: Optional[Callable] = None):

        self.root = root
        self.percent_width = percent_width
        self.percent_height = percent_height
        self.callback_func = callback_func
        self.buttons: list[Button] = []

        # Frame per la barra dei bottoni
        self.button_bar = tk.Frame(
            master=root,
            bg=color
        )
        self.button_bar.pack(
            side = "left", 
            fill = "y"
        )
        self.button_bar.columnconfigure(
            0, weight = 1
        )

        self.add_buttons()
        self.update_size()


    def add_buttons(self):
        # Crea i pulsanti specifici e li aggiunge alla barra
        bar_width = self.root.winfo_width() * self.percent_width
        bar_height = self.root.winfo_height() * self.percent_height

        button_width, button_height = bar_width * 0.9, bar_height * 0.1

        # Aggiungi i pulsanti alla barra
        button1 = RectangleButton(
            self.button_bar, button_width, button_height, "blue", callback_func=lambda: self.callback_func('rectangle')
        )
        button2 = CancelButton(
            self.button_bar, button_width, button_height, "red", callback_func=lambda: self.callback_func('cancel')
        )
        button3 = OpenButton(
            self.button_bar, button_width, button_height, "green", callback_func=lambda: self.callback_func('open')
        )
        button4 = SafeZoneButton(
            self.button_bar, button_width, button_height, "orange", callback_func=lambda: self.callback_func('safezone')
        )
        button5 = FileBackground(
            self.button_bar, button_width, button_height, "yellow", callback_func=lambda: self.callback_func('filebackground')
        )

        button1.grid(row=0, sticky="ew", padx=5, pady=5)
        button2.grid(row=1, sticky="ew", padx=5, pady=5)
        button3.grid(row=2, sticky="ew", padx=5, pady=5)
        button4.grid(row=3, sticky="ew", padx=5, pady=5)
        button5.grid(row=4, sticky="ew", padx=5, pady=5)

        self.buttons.extend([button1, button2, button3, button4, button5])

    
    def update_size(self, event: tk.Event = None):

        # Calcola le nuove dimensioni e aggiorna la posizione
        bar_width = self.root.winfo_width() * self.percent_width
        bar_height = self.root.winfo_height() * self.percent_height

        self.button_bar.config(
            width = bar_width, 
            height = bar_height
        )
        self.button_bar.pack(
            side = "left", 
            fill = "y"
        )


