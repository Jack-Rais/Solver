import tkinter as tk
from . import Mode



class OpenMode(Mode):

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

                if self.last_node['id'] == node['id']:
                    
                    self.canvas.itemconfig(node['id'], outline = 'blue')
                    self.last_node = None

                else:

                    self.canvas.itemconfig(node['id'], outline = 'blue')
                    self.canvas.itemconfig(self.last_node['id'], outline = 'blue')

                    if self.last_node['id'] in [x[0] for x in node['edges']]:

                        id_line = [x[1] for x in node['edges'] if x[0] == self.last_node['id']][0]

                        self.last_node['edges'].remove((node['id'], id_line))
                        node['edges'].remove((self.last_node['id'], id_line))

                        self.canvas.delete(id_line)
                    
                    else:

                        id_edge = self.draw_connection(self.last_node, node)

                        if id_edge:
                            
                            self.open_popup()

                            while self.last_capacity is None:
                                self.canvas.winfo_toplevel().update()

                            self.last_node['edges'].append((node['id'], id_edge, self.last_capacity))
                            node['edges'].append((self.last_node['id'], id_edge, self.last_capacity))

                    self.last_node = None

            else:

                self.canvas.itemconfig(node['id'], outline = 'green')
                self.last_node = node

    
    def open_popup(self):

        popup = tk.Toplevel()
        popup.title("Capacità collegamento massima")
        popup.geometry("300x200")

        label = tk.Label(popup, text="Inserisci la capacità massima del collegamento:")
        label.pack(pady=10)

        entry = tk.Entry(popup)
        entry.pack(pady=10)

        error_label = tk.Label(popup, text="", fg="red")
        error_label.pack(pady=5)

        def get_capacity():

            capacity = entry.get()
            if capacity.isdigit():

                self.last_capacity = int(capacity)
                popup.destroy()

            else:

                error_label.config(text="Per favore, inserisci un numero valido.")

        button = tk.Button(popup, text="Conferma", command=get_capacity)
        button.pack(pady=10)


    
    def are_rectangles_adjacent(self, rect1, rect2):

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
                
        if contact_points[0][0] == contact_points[1][0] and \
            contact_points[0][1] == contact_points[1][1]:

            return False, []

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
            fill = 'red'
        )

        return id_line
        

    def unbind(self):
        self.canvas.unbind('<Button-1>')


    def __call__(self, canvas:tk.Canvas,
                       nodes:list | None = None):
        
        self.canvas = canvas
        self.nodes = nodes if nodes else []

        self.last_node = None
        self.last_capacity = None

        self.canvas.bind('<Button-1>', self.on_mouse_touch)

        return self
    