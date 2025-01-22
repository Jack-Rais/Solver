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

        
    def are_rectangles_adjacent_safezone(self, rect1, rect2):
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
    

    def draw_connection_safezone(self, node1, node2):
        """Disegna una connessione tra due nodi."""

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1)
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2)

        contact, where, type_contact = self.are_rectangles_adjacent_safezone(
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
        
    
    def get_node_by_id(self, id):

        for node in self.graph.nodes(data = True):

            if node[0] == id:
                return node[1]['node']
            
    
    def get_id_by_node(self, node):

        for node_list, idx in self.nodes:

            if node_list == node:
                return idx

    
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

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1)
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2)

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


    def set_graph(self, graph:nx.Graph):

        for node, idx in self.nodes:
            self.canvas.delete(idx)

        self.graph = graph
        self.nodes = self.nodes = [[node[1]['node'], None] for node in graph.nodes(data = True)]

        self.draw_graph()

