import tkinter as tk
import networkx as nx


class CanvasVisualizer:

    def __init__(self, parent:tk.Tk,
                       graph:nx.Graph | None = None):

        self.graph = graph

        if graph:
            self.nodes = [[node[1]['node'], None] for node in graph.nodes(data = True)]
        else:
            self.nodes = []

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(
            parent,
            bg = "white",
            highlightthickness = 0
        )
        self.canvas.grid(column=1, row=0, sticky="nsew",  padx=2, pady=2)

        if graph:
            self.draw_graph()

        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()

        self.canvas.bind("<Configure>", self.__on_resize)

    
    def __on_resize(self, event:tk.Event):

        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height

        self.height = int(event.height)
        self.width = int(event.width)

        self.canvas.scale("all", 0, 0, wscale, hscale)

    
    def set_element(self, element, position, last_position):

        idx = self.nodes.index([element, last_position])
        self.nodes[idx][1] = position
    

    def draw_graph(self):

        for node, id_rect in self.nodes:

            startx, starty, endx, endy = node.pos

            if id_rect:

                self.canvas.delete(id_rect)

                new_id_rect = self.canvas.create_rectangle(
                    startx * self.canvas.winfo_width(),
                    starty * self.canvas.winfo_height(),
                    endx * self.canvas.winfo_width(),
                    endy * self.canvas.winfo_height()
                )

                self.set_element(node, new_id_rect, id_rect)

            else:

                new_id_rect = self.canvas.create_rectangle(
                    startx * self.canvas.winfo_width(),
                    starty * self.canvas.winfo_height(),
                    endx * self.canvas.winfo_width(),
                    endy * self.canvas.winfo_height()
                )

                self.set_element(node, new_id_rect, id_rect)

        for node1, node2 in self.graph.edges():

            res = self.draw_connection(
                self.get_id_by_node(self.get_node_by_id(node1)),
                self.get_id_by_node(self.get_node_by_id(node2))
            )

            if not res:
                self.draw_connection_safezone(
                    self.get_id_by_node(self.get_node_by_id(node1)),
                    self.get_id_by_node(self.get_node_by_id(node2))
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



    def draw_connection_safezone(self, node1, node2):
        """Disegna una connessione tra due nodi."""

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1)
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2)

        contact, where, type_contact = self.__get_adjacency(
            ((x1_1, y1_1), (x2_1, y2_1)),
            ((x1_2, y1_2), (x2_2, y2_2)),
            allow_distance = True
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

        id_line = self.canvas.create_line(*points, width=2, fill='green')
        return id_line
        
    
    def get_node_by_id(self, id):

        for node in self.graph.nodes(data = True):

            if node[0] == id:
                return node[1]['node']
            
    
    def get_id_by_node(self, node):

        for node_list, idx in self.nodes:

            if node_list.id == node.id:
                return idx
            
    
    def get_node_by_id_in(self, id):

        for node_list, idx in self.nodes:
            if id == idx:
                return node_list


    
    def draw_connection(self, node1, node2):
        """Disegna una connessione tra due nodi."""

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1)
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2)

        contact, where, type_contact = self.__get_adjacency(
            ((x1_1, y1_1), (x2_1, y2_1)),
            ((x1_2, y1_2), (x2_2, y2_2)),
            allow_distance = False
        )

        if not contact:
            return False

        (x1, y1), (x2, y2) = where
        x_pos = (x1 + x2) / 2
        y_pos = (y1 + y2) / 2


        '''
        node1 = self.get_node_by_id_in(node1)
        node2 = self.get_node_by_id_in(node2)


        if type_contact == 'verticale':
            print(type_contact)

            print(x_pos, y_pos)
            
            x_start, y_start, x_end, y_end = node1.pos
            width1 = abs(y_start - y_end) * self.canvas.winfo_width()

            x_start, y_start, x_end, y_end = node2.pos
            width2 = abs(y_start - y_end) * self.canvas.winfo_width()

            width_line = min(width1, width2) // 2

            id_line = self.canvas.create_line(
                x_pos, y_pos - width_line,
                x_pos, y_pos + width_line,
                fill = 'red',
                width = 3
            )

        else:

            x_start, y_start, x_end, y_end = node1.pos
            width1 = abs(x_start - x_end) * self.canvas.winfo_width()

            x_start, y_start, x_end, y_end = node2.pos
            width2 = abs(x_start - x_end) * self.canvas.winfo_width()

            width_line = min(width1, width2) // 2

            id_line = self.canvas.create_line(
                x_pos - width_line, y_pos,
                x_pos + width_line, y_pos,
                fill = 'red',
                width = 3
            )'''

        x_pos1, y_pos1 = (x1_1 + x2_1) / 2, (y1_1 + y2_1) / 2
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

        id_line = self.canvas.create_line(*punti, width=2, fill='red')
        return id_line


    def set_graph(self, graph:nx.Graph):

        self.canvas.delete('all')

        self.graph = graph
        self.nodes = [[node[1]['node'], None] for node in graph.nodes(data = True)]

        self.draw_graph()

