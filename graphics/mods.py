import tkinter as tk
from typing import Callable

class Mode:

    def __call__(self, canvas:tk.Canvas,
                       nodes:list | None = None,
                       on_node:Callable | None = None):

        raise NotImplementedError("You need to subscribe the method __call__")
    

class RectangleMode(Mode):

    def closest_x_y(self, posx:int, posy:int):

        closest_x_distance = float('inf')
        closest_y_distance = float('inf')

        closest_x = None
        closest_y = None
        
        for rect in self.nodes:
            xs, ys, xe, ye = self.canvas.coords(rect['id'])

            if abs(xs - posx) < closest_x_distance:
                closest_x = xs
                closest_x_distance = abs(xs - posx)

            if abs(xe - posx) < closest_x_distance:
                closest_x = xe
                closest_x_distance = abs(xe - posx)

            
            if abs(ys - posy) < closest_y_distance:
                closest_y = ys
                closest_y_distance = abs(ys - posy)

            if abs(ye - posy) < closest_y_distance:
                closest_y = ye
                closest_y_distance = abs(ye - posy)

        return closest_x, closest_y, closest_x_distance, closest_y_distance

    def on_mouse_press(self, event:tk.Event):

        self.current_start_x = event.x
        self.current_start_y = event.y

        closest_x, closest_y, closest_x_distance, closest_y_distance = self.closest_x_y(
            self.current_start_x, self.current_start_y
        )
        
        if closest_x and closest_y:

            if closest_x_distance < 10:
                self.current_start_x = closest_x

            if closest_y_distance < 10:
                self.current_start_y = closest_y


        self.rect_id = self.canvas.create_rectangle(
            self.current_start_x, 
            self.current_start_y, 
            self.current_start_x, 
            self.current_start_y, 
            outline = "blue", 
            width = 2
        )

    
    def on_mouse_motion(self, event:tk.Event):

        if self.rect_id:
            self.current_end_x = event.x
            self.current_end_y = event.y

            self.canvas.coords(
                self.rect_id, self.current_start_x, self.current_start_y, event.x, event.y
            )

    
    def on_mouse_release(self, event:tk.Event):

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
            self.current_start_x, 
            self.current_start_y,
            self.current_end_x,
            self.current_end_y
        )

        new_node = {
            'id': self.rect_id,
            'edges': []
        }
        self.nodes.append(new_node)

        self.rect_id = None

    
    def unbind(self):

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')


    def __call__(self, canvas:tk.Canvas, 
                       nodes:list | None = None):
        
        self.canvas = canvas
        self.nodes = [] if nodes is None else nodes

        self.current_start_x = None
        self.current_start_y = None

        self.current_end_x = None
        self.current_end_y = None

        self.rect_id = None

        self.canvas.bind('<Button-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

        return self
    


class CancelMode(Mode):

    def on_mouse_touch(self, event:tk.Event):

        for rect in self.nodes:

            rect_id = rect.get("id")
            coords = self.canvas.coords(rect_id)
            x1, y1, x2, y2 = coords

            if x1 <= event.x <= x2 and y1 <= event.y <= y2:

                self.canvas.delete(rect_id)
                self.nodes.remove(rect)

                break

    def unbind(self):

        self.canvas.unbind('<Button-1>')


    def __call__(self, canvas:tk.Canvas,
                       nodes:list[dict] | None = None):
        
        self.canvas = canvas
        self.nodes = nodes if nodes else []

        self.canvas.bind('<Button-1>', self.on_mouse_touch)

        return self
    

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
                            self.last_node['edges'].append((node['id'], id_edge))
                            node['edges'].append((self.last_node['id'], id_edge))

                    self.last_node = None

            else:

                self.canvas.itemconfig(node['id'], outline = 'green')
                self.last_node = node

    
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

        self.canvas.bind('<Button-1>', self.on_mouse_touch)

        return self
    