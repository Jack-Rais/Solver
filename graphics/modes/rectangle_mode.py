import tkinter as tk

from ..utils import Popup
from .base_mode import Mode


class RectangleMode(Mode):

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self.rect_id = None
        self.last_capacity = None
        self.last_id = None

        # Coordinate della selezione
        self.current_start_x = None
        self.current_start_y = None
        self.current_end_x = None
        self.current_end_y = None

        self.canvas.config(
            cursor = 'crosshair'
        )

        # Associa i metodi agli eventi
        self.canvas.bind('<Button-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)


    def on_mouse_press(self, event: tk.Event):
        """Gestisce il click del mouse per iniziare la selezione del rettangolo."""

        self.current_start_x, self.current_start_y = event.x, event.y
        
        closest_x, closest_y, closest_x_distance, closest_y_distance = self.closest_x_y(
            self.current_start_x, self.current_start_y
        )
        
        if closest_x and closest_y:

            if closest_x_distance < 10:
                self.current_start_x = closest_x

            if closest_y_distance < 10:
                self.current_start_y = closest_y
        

        # Crea il rettangolo
        self.rect_id = self.canvas.create_rectangle(
            self.current_start_x, self.current_start_y,
            self.current_start_x, self.current_start_y,
            outline = "blue", width = 2
        )

    
    def on_mouse_motion(self, event: tk.Event):
        """Gestisce il movimento del mouse per disegnare un rettangolo."""

        if self.rect_id:

            # Riposiziona il rettangolo dove è cliccato il mouse
            self.current_end_x = event.x
            self.current_end_y = event.y

            self.canvas.coords(
                self.rect_id, 
                self.current_start_x, 
                self.current_start_y, 
                self.current_end_x, 
                self.current_end_y
            )


    def on_mouse_release(self, event: tk.Event):
        """Gestisce il rilascio del mouse per finalizzare il rettangolo e mostrare il pop-up."""

        closest_x, closest_y, closest_x_distance, closest_y_distance = self.closest_x_y(
            event.x, event.y
        )
        
        if closest_x and closest_y:

            if closest_x_distance < 10:
                self.current_end_x = closest_x

            if closest_y_distance < 10:
                self.current_end_y = closest_y
        

        self.canvas.coords(
            self.rect_id,
            self.current_start_x, self.current_start_y,
            self.current_end_x, self.current_end_y
        )

        # Usa il Popup
        def handle_input(inputs):
            self.last_capacity = int(inputs['capacity'])
            self.last_id = inputs['id']
            self.create_node()

        fields = [
            {"label": "ID della stanza", "name": "id"},
            {"label": "Capacità della stanza", "name": "capacity"}
        ]
        Popup(
            title="Capacità stanza massima",
            label="Inserisci l'ID e la capacità della stanza:",
            fields=fields,
            callback=handle_input
        )

    
    def closest_x_y(self, posx: int, posy: int):
        """Trova il punto più vicino a (posx, posy) tra i nodi."""

        closest_x_distance = float('inf')
        closest_y_distance = float('inf')
        closest_x, closest_y = None, None

        for rect in self.nodes:
            xs, ys, xe, ye = self.canvas.coords(rect['id'])

            if abs(xs - posx) < closest_x_distance:
                closest_x, closest_x_distance = xs, abs(xs - posx)

            if abs(xe - posx) < closest_x_distance:
                closest_x, closest_x_distance = xe, abs(xe - posx)

            if abs(ys - posy) < closest_y_distance:
                closest_y, closest_y_distance = ys, abs(ys - posy)

            if abs(ye - posy) < closest_y_distance:
                closest_y, closest_y_distance = ye, abs(ye - posy)

        return closest_x, closest_y, closest_x_distance, closest_y_distance


    def create_node(self):
        """Crea il nodo con i valori raccolti."""

        new_node = {
            'id': self.rect_id,
            'edges': [],
            'capacity': self.last_capacity,
            'nome_stanza': self.last_id,
            'type': 'node'
        }
        self.nodes.append(new_node)
        self.rect_id = self.last_id = None

    
    def unbind(self):

        self.canvas.config(
            cursor = 'arrow'
        )

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

    
    def pass_args(self):
        
        return {
            'canvas': self.canvas,
            'nodes': self.nodes,
            'background': self.background
        }