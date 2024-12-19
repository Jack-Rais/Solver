import tkinter as tk

class DragRectangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disegna Rettangolo con Trascinamento")

        # Creazione del Canvas
        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Variabili per il punto iniziale e il rettangolo corrente
        self.start_x = None
        self.start_y = None
        self.rect_id = None

        # Binding degli eventi del mouse
        self.canvas.bind("<Button-1>", self.on_mouse_press)   # Mouse premuto
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)   # Mouse trascinato
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)  # Mouse rilasciato

    def on_mouse_press(self, event):
        """ Inizia a disegnare il rettangolo. """
        self.start_x = event.x
        self.start_y = event.y

        # Crea un rettangolo iniziale
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)

    def on_mouse_drag(self, event):
        """ Aggiorna il rettangolo mentre il mouse viene trascinato. """
        if self.rect_id:
            # Aggiorna il rettangolo dinamicamente con le nuove coordinate
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_release(self, event):
        """ Termina il disegno del rettangolo al rilascio del mouse. """
        self.rect_id = None  # Nessun rettangolo attivo

# Crea la finestra principale
if __name__ == "__main__":
    root = tk.Tk()
    app = DragRectangleApp(root)
    root.mainloop()
