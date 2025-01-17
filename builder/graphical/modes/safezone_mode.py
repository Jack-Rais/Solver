import tkinter as tk

from .base_mode import Mode
from ..utils import Popup

from ...network.bases import Node
from ...network.lists import ListEdges


class SafeZoneMode(Mode):


    def __init__(self, **kwargs):
        """Inizializza la modalità zona sicura."""

        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.last_capacity = None
        self.connection_capacity = None
        self.last_node:Node = None
        self.last_id = None

        # Binding degli eventi
        self.canvas.bind('<Button-1>', self.on_mouse_touch)


    def on_mouse_touch(self, event: tk.Event):
        """Gestisce il click del mouse per selezionare e connettere i nodi."""

        node = self.is_in(event.x, event.y)

        if node and self.last_node:
            
            self.canvas.itemconfig(self.last_node.id, outline='blue')
            
            self.last_node = node
            self.canvas.itemconfig(node.id, outline='yellow')

        elif node and not self.last_node:
            
            self.last_node = node
            self.canvas.itemconfig(node.id, outline='yellow')

        elif self.last_node and not node:
            self.handle_new_node(event)

        else:
            print('Non hai selezionato la posizione dal quale si può accedere alla zona sicura')


    def is_in(self, x, y):
        """Verifica se il click è all'interno di un nodo."""

        for node in self.nodes:

            x1, y1, x2, y2 = self.canvas.coords(node.id)
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)

            if x_min <= x <= x_max and y_min <= y <= y_max:
                return node
            
        return False


    def handle_new_node(self, event:tk.Event):
        """Gestisce la creazione di un nuovo nodo."""

        x1, y1, x2, y2 = self.canvas.coords(self.last_node['id'])
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        if x1 < event.x < x2 or y1 < event.y < y2:

            outside_node = self.canvas.create_oval(
                event.x - 15, event.y - 15, event.x + 15, event.y + 15,
                outline='green', width=3
            )

            self.open_popup()
            while self.last_capacity is None and self.connection_capacity is None:
                self.canvas.winfo_toplevel().update()


            new_node = self.nodes.add_node(
                outside_node,
                edges = ListEdges(),
                capacity = -self.last_capacity,
                nome_stanza = self.last_id(outside_node),
                type = 'safezone'
            )

            id_edge = self.draw_connection(self.last_node, new_node)

            new_node.add_edge(self.last_node.id, id_edge, self.connection_capacity)
            self.last_node.add_edge(new_node.id, id_edge, self.connection_capacity)

            self.last_capacity = None
            self.connection_capacity = None
            self.canvas.itemconfig(self.last_node.id, outline='blue')

        self.last_node = None


    def open_popup(self):
        """Apre un popup per inserire la capacità e l'id della zona sicura."""


        def callback(inputs:dict):
            """Callback per gestire l'inserimento della capacità e dell'id."""

            try:
                self.last_capacity = int(inputs.get('capacita', 0))
                self.connection_capacity = int(inputs.get('capacita_connessione', 0))

                # Usa id fornito o quello di default
                self.last_id = inputs.get('id_zona', '<>')
                self.last_id = lambda x: x if self.last_id == '<>' else self.last_id

            except ValueError:
                self.last_capacity = None
                self.connection_capacity = None


        # Crea il popup con i campi per la capacità e l'id
        fields = [
            {'label': 'Capacità della zona sicura', 'name': 'capacita'},
            {'label': 'Capacità della connessione', 'name': 'capacita_connessione'},
            {'label': 'ID della zona sicura', 'name': 'id_zona'}
        ]

        self.popup = Popup(
            title = "Capacità zona sicura",
            label = "Inserisci i dati della zona sicura e della connessione:",
            fields = fields,
            callback = callback
        )


    def are_rectangles_adjacent(self, rect1, rect2):
        """Verifica se due rettangoli sono adiacenti."""

        def normalize(rect):
            (x1, y1), (x2, y2) = rect
            return (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))
        

        (x1_min, y1_min), (x1_max, y1_max) = normalize(rect1)
        (x2_min, y2_min), (x2_max, y2_max) = normalize(rect2)

        contact_points = []
        type_contact = None


        if y1_min < y2_min < y1_max or y1_min < y2_max < y1_max:

            overlap_min = max(y1_min, y2_min)
            overlap_max = min(y1_max, y2_max)
            type_contact = 'orizzontale'

            if overlap_min <= overlap_max:
                contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)] if x1_max == x2_min \
                    else [(x1_min, overlap_min), (x1_min, overlap_max)]

        elif x1_min < x2_min < x1_max or x1_min < x2_max < x1_max:

            overlap_min = max(x1_min, x2_min)
            overlap_max = min(x1_max, x2_max)
            type_contact = 'verticale'

            if overlap_min <= overlap_max:
                contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)] if y1_max == y2_min \
                    else [(overlap_min, y1_min), (overlap_max, y1_min)]


        if not contact_points:
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
            points = [
                x_pos1, y_pos1,
                x_pos, y_pos1,
                x_pos, y_pos2,
                x_pos2, y_pos2
            ]
        else:
            points = [
                x_pos1, y_pos1,
                x_pos1, y_pos,
                x_pos2, y_pos,
                x_pos2, y_pos2
            ]

        id_line = self.canvas.create_line(*points, width=2, fill='green')
        return id_line


    def unbind(self):
        """Disassocia gli eventi dal canvas."""

        self.canvas.unbind('<Button-1>')

    
    def pass_args(self):
        
        return {
            'canvas': self.canvas,
            'nodes': self.nodes,
            'background': self.background
        }