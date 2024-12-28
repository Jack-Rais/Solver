import tkinter as tk
from . import Mode


class SafeZoneMode(Mode):


    def on_mouse_touch(self, event:tk.Event):

        def is_in(x, y):

            for node in self.nodes:
                
                x1, y1, x2, y2 = self.canvas.coords(node['id'])
                
                x_min, x_max = min(x1, x2), max(x1, x2)
                y_min, y_max = min(y1, y2), max(y1, y2)
                
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    return node

            return False
        
        
        if isinstance(node := is_in(event.x, event.y), dict):

            if self.last_node:

                self.last_node = None

            else:

                self.last_node = node
                self.canvas.itemconfig(
                    node['id'],
                    outline = 'yellow'
                )

        else:

            if self.last_node:

                x1, y1, x2, y2 = self.canvas.coords(self.last_node['id'])
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)

                if x1 < event.x < x2 or y1 < event.y < y2:

                    outside_node = self.canvas.create_oval(
                        event.x - 15,
                        event.y - 15,
                        event.x + 15,
                        event.y + 15,
                        outline = 'green',
                        width = 3
                    )

                    self.open_popup()
                    while self.last_capacity is None and self.connection_capacity is None:
                        self.canvas.winfo_toplevel().update()

                    new_node = {
                        'id': outside_node,
                        'edges': [],
                        'capacity': -self.last_capacity,
                        'nome_stanza': self.last_id(outside_node),
                        'type': 'safezone'
                    }

                    id_edge = self.draw_connection(self.last_node, new_node)

                    new_node['edges'].append((self.last_node['id'], id_edge, self.connection_capacity))
                    self.last_node['edges'].append((new_node['id'], id_edge, self.connection_capacity))

                    self.nodes.append(new_node)

                    self.last_capacity = None
                    self.connection_capacity = None
                    self.canvas.itemconfig(
                        self.last_node['id'],
                        outline = 'blue'
                    )
                
                self.last_node = None

            else:
                print('Non hai selezionato la posizione dal quale si può accedere alla zona sicura')


    def open_popup(self):

        popup = tk.Toplevel()
        popup.title("Capacità zona sicura massima")
        popup.geometry("300x200")

        label_id = tk.Label(popup, text="Inserisci l'id della zona sicura:")
        label_id.grid(
            column = 0,
            row = 0
        )

        entry_id = tk.Entry(popup)
        entry_id.grid(
            column = 0,
            row = 1
        )

        label = tk.Label(popup, text="Inserisci la capacità massima della zona sicura:")
        label.grid(
            column = 0,
            row = 2
        )

        entry = tk.Entry(popup)
        entry.grid(
            column = 0,
            row = 3
        )

        label_connection = tk.Label(popup, text="Inserisci la capacità massima della connessione:")
        label_connection.grid(
            column = 0,
            row = 4
        )

        entry_connection = tk.Entry(popup)
        entry_connection.grid(
            column = 0,
            row = 5
        )

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(
            column = 0,
            row = 6
        )

        def get_capacity():

            capacity = entry.get()
            connection_capacity = entry_connection.get()
            id_zone = entry_id.get()

            def get_last_id(x):
                return id_zone if id_zone != '' else x

            if capacity.isdigit():

                self.last_capacity = int(capacity)
                self.connection_capacity = int(connection_capacity) if connection_capacity else 0
                self.last_id = get_last_id
                popup.destroy()

            else:

                error_label.config(text="Per favore, inserisci un numero valido.")

        button = tk.Button(popup, text="Conferma", command=get_capacity)
        button.grid(
            column = 0,
            row = 7
        )


    def are_rectangles_adjacent(self, rect1, rect2):

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
                
        if len(contact_points) == 0:
            return False, [], None
                
        if contact_points[0][0] == contact_points[1][0] and \
            contact_points[0][1] == contact_points[1][1]:

            return False, [], None

        return bool(contact_points), contact_points, type_contact

    
    def draw_connection(self, node1, node2):

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(node1['id'])
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(node2['id'])

        contact, where, type_contact = self.are_rectangles_adjacent(
            ((x1_1, y1_1), (x2_1, y2_1)),
            ((x1_2, y1_2), (x2_2, y2_2))
        )

        if not contact:
            return False
        
        (x1, y1), (x2, y2) = where
        x_pos, y_pos = (x1 + x2) / 2, (y1 + y2) / 2

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

        id_line = self.canvas.create_line(
            *punti,
            width = 2,
            fill = 'green'
        )

        return id_line


    def unbind(self):
        self.canvas.unbind('<Button-1>')


    def __call__(self, canvas:tk.Canvas, 
                       nodes:list | None = None):
        
        self.canvas = canvas
        self.nodes = [] if nodes is None else nodes

        self.last_capacity = None
        self.connection_capacity = None
        self.last_node = None
        self.last_id = None

        self.canvas.bind('<Button-1>', self.on_mouse_touch)

        return self