import tkinter as tk
from typing import Callable

class Popup:

    def __init__(self, title: str, 
                       label: str, 
                       fields: list[str], 
                       callback: Callable):

        self.title = title
        self.label = label
        self.fields = fields
        self.callback = callback
        self.popup: tk.Toplevel = None
        self.entries: dict[str, tk.Entry] = {}
        self.create_popup()


    def create_popup(self):
        """Crea il pop-up con i campi e il pulsante di conferma."""

        self.popup = tk.Toplevel()
        self.popup.title(self.title)
        self.popup.geometry("300x200")


        label = tk.Label(self.popup, text=self.label)
        label.grid(column = 0, row = 0)

        # Creazione dei campi di input
        row = 1
        for field in self.fields:

            label = tk.Label(self.popup, text = field["label"])
            label.grid(column = 0, row = row)

            entry = tk.Entry(self.popup)
            entry.grid(column = 0, row = row + 1)
            self.entries[field["name"]] = entry

            row += 2

        # Pulsante per confermare
        button = tk.Button(self.popup, text="Conferma", command=self.on_confirm)
        button.grid(column = 0, row = row)


    def on_confirm(self):
        """Gestisce la conferma del pop-up."""

        inputs = {}
        valid = True
        for name, entry in self.entries.items():
            value = entry.get()

            if value.strip() == "":
                valid = False
                break

            inputs[name] = value
        
        if valid:
            self.callback(inputs)
            self.popup.destroy()
            
        else:
            # Mostra un messaggio di errore se i dati non sono validi
            error_label = tk.Label(self.popup, text="Per favore, inserisci valori validi", fg="red")
            error_label.grid(column=0, row=len(self.fields) * 2 + 1)


    def center_app(self, root: tk.Toplevel, width: int, height: int) -> None:

        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()

        posx = (screen_width - width) // 2
        posy = (screen_height - height) // 2

        root.geometry(f'{width}x{height}+{posx}+{posy}')
        root.update()