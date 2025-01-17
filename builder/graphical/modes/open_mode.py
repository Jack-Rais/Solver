import tkinter as tk

from .base_mode import Mode
from ..utils import Popup


class OpenMode(Mode):


    def __init__(self, **kwargs):
        """Inizializza la modalità di apertura."""

        for key, value in kwargs.items():
            setattr(self, key, value)

        
        self.last_node = None
        self.last_capacity = None

        # Binding degli eventi
        self.canvas.bind('<Button-1>', self.on_mouse_touch)


    def on_mouse_touch(self, event: tk.Event):
        """Gestisce il click del mouse per selezionare e connettere i nodi."""

        node = self.get_node_at(event.x, event.y)
        
        if isinstance(node, dict):  # Se è stato selezionato un nodo
            self.handle_node_click(node, event)


    def get_node_at(self, x, y):
        """Verifica se il click è all'interno di un nodo."""

        for node in self.nodes:

            x1, y1, x2, y2 = self.canvas.coords(node['id'])
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)

            if x_min <= x <= x_max and y_min <= y <= y_max:
                return node
            
        return None


    def handle_node_click(self, node, event):
        """Gestisce il comportamento dopo il click su un nodo."""

        if self.last_node:

            if self.last_node['id'] == node['id']:
                self.canvas.itemconfig(node['id'], outline = 'blue')
                self.last_node = None

            else:

                self.canvas.itemconfig(node['id'], outline = 'blue')
                self.canvas.itemconfig(self.last_node['id'], outline = 'blue')

                self.handle_edge_creation(node)
                self.last_node = None

        else:
            self.canvas.itemconfig(node['id'], outline='green')
            self.last_node = node


    def handle_edge_creation(self, node):
        """Gestisce la creazione o la rimozione di un edge tra i nodi."""

        if self.last_node['id'] in [x[0] for x in node['edges']]:

            id_line = [x[1] for x in node['edges'] if x[0] == self.last_node['id']][0]
            self.last_node['edges'].remove((node['id'], id_line))
            node['edges'].remove((self.last_node['id'], id_line))
            self.canvas.delete(id_line)

        else:
            id_edge = self.draw_connection(self.last_node, node)

            if id_edge:
                self.open_popup()

                # Attendi che l'utente inserisca la capacità
                while self.last_capacity is None:
                    self.canvas.winfo_toplevel().update()

                self.last_node['edges'].append((node['id'], id_edge, self.last_capacity))
                node['edges'].append((self.last_node['id'], id_edge, self.last_capacity))

                self.last_capacity = None


    def are_rectangles_adjacent(self, rect1, rect2):
        """Restituisce se i due rettangoli si toccano, in quali punti e in quale direzione"""

        def normalize(rect):
            (x1, y1), (x2, y2) = rect
            return (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))

        (x1_min, y1_min), (x1_max, y1_max) = normalize(rect1)
        (x2_min, y2_min), (x2_max, y2_max) = normalize(rect2)

        contact_points = []
        type_contact = None

        if x1_max == x2_min or x1_min == x2_max:

            overlap_min = max(y1_min, y2_min)
            overlap_max = min(y1_max, y2_max)

            type_contact = 'orizzontale'

            if overlap_min <= overlap_max:
                contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)] if x1_max == x2_min \
                    else [(x1_min, overlap_min), (x1_min, overlap_max)]

        elif y1_max == y2_min or y1_min == y2_max:

            overlap_min = max(x1_min, x2_min)
            overlap_max = min(x1_max, x2_max)

            type_contact = 'verticale'
            
            if overlap_min <= overlap_max:
                contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)] if y1_max == y2_min \
                    else [(overlap_min, y1_min), (overlap_max, y1_min)]
                
        if len(contact_points) == 0:
            return False, [], None
                
        if contact_points[0][0] == contact_points[1][0] and \
            contact_points[0][1] == contact_points[1][1]:

            return False, [], None

        return bool(contact_points), contact_points, type_contact


    def draw_connection(self, node1, node2):
        """Disegna una connessione tra due nodi."""

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1['id'])
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2['id'])

        contact, where, type_contact = self.are_rectangles_adjacent(
            ((x1_1, y1_1), (x2_1, y2_1)),
            ((x1_2, y1_2), (x2_2, y2_2))
        )

        if not contact:
            return False

        (x1, y1), (x2, y2) = where
        x_pos = (x1 + x2) / 2
        y_pos = (y1 + y2) / 2

        x_pos1, y_pos1 = (x1_1 + x2_1) / 2, (y1_1 + y2_1) / 2
        x_pos2, y_pos2 = (x1_2 + x2_2) / 2, (y1_2 + y2_2) / 2

        if type_contact == 'verticale':
            punti = [
                x_pos1, y_pos1,
                x_pos, y_pos1,
                x_pos, y_pos2,
                x_pos2, y_pos2
            ]
        else:
            punti = [
                x_pos1, y_pos1,
                x_pos1, y_pos,
                x_pos2, y_pos,
                x_pos2, y_pos2
            ]

        id_line = self.canvas.create_line(*punti, width=2, fill='red')
        return id_line

    def open_popup(self):
        """Apre un popup per inserire la capacità della connessione."""


        def callback(inputs):
            """Callback per gestire l'inserimento della capacità."""

            try:
                self.last_capacity = float(inputs.get('capacita', 0))
            except ValueError:
                self.last_capacity = None


        # Crea il popup con un campo per la capacità
        fields = [{'label': 'Capacità del collegamento', 'name': 'capacita'}]
        self.popup = Popup(
            title = "Capacità collegamento massima",
            label = "Inserisci la capacità massima del collegamento:",
            fields = fields,
            callback = callback
        )

    def unbind(self):
        """Disassocia gli eventi dal canvas."""

        self.canvas.unbind('<Button-1>')


    def pass_args(self):
        
        return {
            'canvas': self.canvas,
            'nodes': self.nodes,
            'background': self.background
        }