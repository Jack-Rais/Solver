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
            'pos': self.canvas.coords(self.rect_id)
        }
        self.nodes.append(new_node)
        self.on_node_add(new_node)

        self.rect_id = None

    
    def unbind(self):

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')


    def __call__(self, canvas:tk.Canvas, 
                       nodes:list | None = None,
                       on_node:Callable | None = None):
        
        self.canvas = canvas
        self.nodes = [] if nodes is None else nodes

        self.current_start_x = None
        self.current_start_y = None

        self.current_end_x = None
        self.current_end_y = None

        self.current_rect_id = None

        self.on_node_add = on_node if on_node else lambda x: x

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

                self.on_node_delete(rect)

                break

    def unbind(self):

        self.canvas.unbind('<Button-1>')


    def __call__(self, canvas:tk.Canvas,
                       nodes:list[dict] | None = None,
                       on_node:Callable | None = None):
        
        self.canvas = canvas
        self.nodes = nodes if nodes else []

        self.on_node_delete = on_node if on_node else lambda x: x

        self.canvas.bind('<Button-1>', self.on_mouse_touch)

        return self
    

class OpenMode(Mode):

    def __call__(self, canvas:tk.Canvas,
                       nodes:list | None = None,
                       on_node:Callable | None = None):
        
        self.canvas = canvas
        self.nodes = nodes if nodes else []
        self.on_arch_creation = on_node


    