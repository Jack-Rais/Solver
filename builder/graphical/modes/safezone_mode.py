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

        x1, y1, x2, y2 = self.canvas.coords(self.last_node.id)
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
                units_count = -self.last_capacity,
                capacity = -self.last_capacity,
                name = self.last_id,
                type = 'safezone',
                position = (
                    (event.x - 15) / self.canvas.winfo_width(), 
                    (event.y - 15) / self.canvas.winfo_height(),
                    (event.x + 15) / self.canvas.winfo_width(), 
                    (event.y + 15) / self.canvas.winfo_height()
                )
            )

            id_edge = self.draw_connection(self.last_node, new_node)

            new_node.add_edge(self.last_node.id, id_edge, self.connection_capacity)
            self.last_node.add_edge(new_node.id, id_edge, self.connection_capacity)

            self.nodes.add_edge(
                new_node.id, 
                self.last_node.id, 
                id_edge,
                self.connection_capacity
            )

            self.last_capacity = None
            self.connection_capacity = None
            self.canvas.itemconfig(
                self.last_node.id, 
                outline = 'blue'
            )

        self.last_node = None


    def open_popup(self):
        """Apre un popup per inserire la capacità e l'id della zona sicura."""


        def callback(inputs:dict):
            """Callback per gestire l'inserimento della capacità e dell'id."""

            try:
                self.last_id = inputs.get('id_zona', '<>')
                self.last_capacity = int(inputs.get('capacita', 0))
                self.connection_capacity = float(inputs.get('capacita_connessione', 0))


            except ValueError:
                self.last_capacity = None
                self.connection_capacity = None


        # Crea il popup con i campi per la capacità e l'id
        fields = [
            {'label': 'ID della zona sicura', 'name': 'id_zona'},
            {'label': 'Capacità della zona sicura', 'name': 'capacita'},
            {'label': 'Capacità della connessione', 'name': 'capacita_connessione'}
        ]

        self.popup = Popup(
            title = "Capacità zona sicura",
            label = "Inserisci i dati della zona sicura e della connessione:",
            fields = fields,
            callback = callback
        )

    def __get_adjacency(self, rect1, rect2, allow_distance):
        """
        Determines whether two rectangles are adjacent and, optionally, their proximity if not touching.

        Args:
            rect1 (Tuple[Tuple[int, int], Tuple[int, int]]): First rectangle ((x_min, y_min), (x_max, y_max)).
            rect2 (Tuple[Tuple[int, int], Tuple[int, int]]): Second rectangle ((x_min, y_min), (x_max, y_max)).
            allow_distance (bool): If True, considers proximity even when rectangles do not touch.

        Returns:
            Tuple:
                - bool: True if rectangles are adjacent or close (depending on `allow_distance`).
                - List[Tuple[int, int], Tuple[int, int]]: List of contact points (if any).
                - Optional[Literal['horizontal', 'vertical']]: Contact direction ('horizontal' or 'vertical'), None if no contact.
        """

        def normalize(rect):
            (x1, y1), (x2, y2) = rect
            return (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))

        (x1_min, y1_min), (x1_max, y1_max) = normalize(rect1)
        (x2_min, y2_min), (x2_max, y2_max) = normalize(rect2)

        contact_points = []
        type_contact = None


        # Check horizontal overlap
        if y1_min < y2_max and y2_min < y1_max:  
            overlap_min, overlap_max = max(y1_min, y2_min), min(y1_max, y2_max)
            
            # If the two rectangles have a contact point
            if x1_max == x2_min or x1_min == x2_max:
                type_contact = 'horizontal'

                # Check if the contact point is on the left or the right
                if x1_max == x2_min:
                    contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)]

                elif x1_min == x2_max:
                    contact_points = [(x1_min, overlap_min), (x1_min, overlap_max)]

            # If the two rectangles are one under the other and the allow_distance is on
            elif allow_distance and overlap_min <= overlap_max:
                type_contact = 'horizontal'

                contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)] if x1_max == x2_min \
                    else [(x1_min, overlap_min), (x1_min, overlap_max)]


        # Check vertical overlap
        elif x1_min < x2_max and x2_min < x1_max:
            overlap_min, overlap_max = max(x1_min, x2_min), min(x1_max, x2_max)

            # If the two rectangles have a contact point
            if y1_max == y2_min or y1_min == y2_max:
                type_contact = 'vertical'

                # Check if the contact point is on the top or the bottom
                if y1_max == y2_min:
                    contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)]

                elif y1_min == y2_max:
                    contact_points = [(overlap_min, y1_min), (overlap_max, y1_min)]

            # If the two rectangles are one after the other and the allow_distance is on
            elif allow_distance and overlap_min <= overlap_max:
                type_contact = 'vertical'

                contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)] if y1_max == y2_min \
                    else [(overlap_min, y1_min), (overlap_max, y1_min)]
                

        # If no contact points were found
        if not contact_points:
            return False, [], None

        # Edge case: If both points are identical, there's no real contact
        if len(contact_points) == 2 and contact_points[0] == contact_points[1]:
            return False, [], None

        return True, tuple(contact_points), type_contact


    def draw_connection(self, node1:Node, node2:Node):
        """Disegna una connessione tra due nodi."""

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1.id)
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2.id)

        contact, where, type_contact = self.__get_adjacency(
            ((x1_1, y1_1), (x2_1, y2_1)),
            ((x1_2, y1_2), (x2_2, y2_2)),
            allow_distance=True
        )

        if not contact:
            return False

        (x1, y1), (x2, y2) = where
        x_pos = (x1 + x2) / 2
        y_pos = (y1 + y2) / 2

        x_pos1, y_pos1 = (x1_1 + x2_1) / 2, (y1_1 + y2_1) / 2
        x_pos2, y_pos2 = (x1_2 + x2_2) / 2, (y1_2 + y2_2) / 2

        if type_contact == 'vertical':
            points = [
                x_pos1, y_pos1,
                x_pos, y_pos1,
                x_pos, y_pos2,
                x_pos2, y_pos2
            ]
        elif type_contact == 'horizontal':
            points = [
                x_pos1, y_pos1,
                x_pos1, y_pos,
                x_pos2, y_pos,
                x_pos2, y_pos2
            ]

        else:
            raise ValueError()

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