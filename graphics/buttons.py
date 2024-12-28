import tkinter as tk


class Button(tk.Button):

    def __init__(self, master, 
                       width, 
                       height, 
                       color, 
                       callback_func = None, 
                       row = 0, 
                       **kwargs):
        
        # Costruttore del pulsante di base
        super().__init__(master, **kwargs)
        
        self.master = master
        self.width = width
        self.height = height
        self.color = color
        self.callback_func = callback_func
        self.row = row
        
        # Configura l'aspetto del pulsante
        self.config(
            bg = color
        )
        
        # Posiziona il pulsante nella sua riga
        self.grid(
            row = row, 
            column = 0, 
            padx = 10, 
            pady = 10
        )
        
        # Imposta il comportamento del clic del pulsante
        if self.callback_func:
            self.config(command = self.callback_func)


class RectangleButton(Button):

    def __init__(self, master, 
                       width, 
                       height, 
                       color, 
                       callback_func = None, 
                       row = 0, 
                       **kwargs):

        # Crea un pulsante di tipo "Rectangle"
        super().__init__(master, width, height, color, callback_func, row, **kwargs)
        self.config(text="Rectangle")


class CancelButton(Button):

    def __init__(self, master, 
                       width, 
                       height, 
                       color, 
                       callback_func = None, 
                       row = 0, 
                       **kwargs):

        # Crea un pulsante di tipo "Cancel"
        super().__init__(master, width, height, color, callback_func, row, **kwargs)
        self.config(text="Cancel")


class OpenButton(Button):
    
    def __init__(self, master, 
                       width, 
                       height, 
                       color, 
                       callback_func = None, 
                       row = 0, 
                       **kwargs):
        
        # Crea un pulsante di tipo "Open"
        super().__init__(master, width, height, color, callback_func, row, **kwargs)
        self.config(text="Open")


class SafeZoneButton(Button):
    
    def __init__(self, master, 
                       width, 
                       height, 
                       color, 
                       callback_func = None, 
                       row = 0, 
                       **kwargs):
        
        # Crea un pulsante di tipo "SafeZone"
        super().__init__(master, width, height, color, callback_func, row, **kwargs)
        self.config(text="SafeZone")
