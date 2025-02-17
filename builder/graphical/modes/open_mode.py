import tkinter as tk

from .base_mode import Mode
from ..utils import Popup

from ...network.bases import Node


class OpenMode(Mode):


    def __init__(self, **kwargs):
        """Inizializza la modalità di apertura."""

        for key, value in kwargs.items():
            setattr(self, key, value)

        
        self.last_node:Node = None
        self.last_capacity = None

        # Binding degli eventi
        self.canvas.bind('<Button-1>', self.on_mouse_touch)


    def on_mouse_touch(self, event: tk.Event):
        """Gestisce il click del mouse per selezionare e connettere i nodi."""

        node = self.get_node_at(event.x, event.y)
        
        if node:  # Se è stato selezionato un nodo
            self.handle_node_click(node)


    def get_node_at(self, x, y):
        """Verifica se il click è all'interno di un nodo."""

        for node in self.nodes:

            x1, y1, x2, y2 = self.canvas.coords(node.id)
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)

            if x_min <= x <= x_max and y_min <= y <= y_max:
                return node
            
        return None


    def handle_node_click(self, node:Node):
        """Gestisce il comportamento dopo il click su un nodo."""

        if self.last_node:

            if self.last_node.id == node.id:
                self.canvas.itemconfig(node.id, outline = 'blue')
                self.last_node = None

            else:

                self.canvas.itemconfig(node.id, outline = 'blue')
                self.canvas.itemconfig(self.last_node.id, outline = 'blue')

                self.handle_edge_creation(node)
                self.last_node = None

        else:
            self.canvas.itemconfig(node.id, outline='green')
            self.last_node = node


    def handle_edge_creation(self, node:Node):
        """Gestisce la creazione o la rimozione di un edge tra i nodi."""

        if node.edges.contains_id(self.last_node.id):

            id_line = node.edges.get_line_by_id(self.last_node.id)
            self.canvas.delete(id_line)

            self.last_node.remove_edge(node.id)
            node.remove_edge(self.last_node.id)

        else:
            id_edge = self.draw_connection(self.last_node, node)

            if id_edge:
                self.open_popup()

                # Attendi che l'utente inserisca la capacità
                while self.last_capacity is None:
                    self.canvas.winfo_toplevel().update()

                self.nodes.add_edge(node.id, self.last_node.id, id_edge, self.last_capacity)
                self.nodes.add_edge(self.last_node.id, node.id, id_edge, self.last_capacity)

                self.last_capacity = None
    

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
            False
        )

        if not contact:
            return False

        (x1, y1), (x2, y2) = where
        x_pos = (x1 + x2) / 2
        y_pos = (y1 + y2) / 2


        '''x_pos1, y_pos1 = (x1_1 + x2_1) / 2, (y1_1 + y2_1) / 2
        x_pos2, y_pos2 = (x1_2 + x2_2) / 2, (y1_2 + y2_2) / 2

        if type_contact == 'vertical':
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

        id_line = self.canvas.create_line(*punti, width=2, fill='red')'''


        if type_contact == 'vertical':

            height_node1 = abs(y1_1 - y1_2)
            height_node2 = abs(y2_1 - y2_2)

            len_line = int(min(height_node1, height_node2) * 0.2)

            id_line = self.canvas.create_line(
                x_pos, 
                y_pos - len_line, 
                x_pos, 
                y_pos + len_line, width=2, fill='red'
            )

        elif type_contact == 'horizontal':

            width_node1 = abs(x1_1 - x1_2)
            width_node2 = abs(x2_1 - x2_2)

            len_line = int(min(width_node1, width_node2) * 0.2)

            id_line = self.canvas.create_line(
                x_pos - len_line,
                y_pos, 
                x_pos + len_line, 
                y_pos, width=2, fill='red'
            )

        else:
            raise ValueError('type_contact must be only "vertical" or "horizontal"')
        
        return id_line
        





        return id_line

    def open_popup(self):
        """Apre un popup per inserire la capacità della connessione."""


        def callback(inputs:dict):
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