import tkinter as tk


class Mode:

    def __call__(self, event:tk.Event):

        raise NotImplementedError("You need to subscribe the method __call__")
    

class RectangleMode(Mode):

    def on_mouse_press(self, event:tk.Event):

        self.start_x = event.x
        self.start_y = event.y

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
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    
    def on_mouse_release(self, event:tk.Event):
        self.rect_id = None

    
    def unbind(self):

        self.canvas.unbind('<Button1>')
        self.canvas.bind('<B1-Motion>')
        self.canvas.bind('<ButtonRelease-1>')


    def __call__(self, canvas:tk.Canvas):
        
        self.canvas = canvas

        self.current_start_x = None
        self.current_start_y = None
        self.current_rect_id = None

        self.canvas.bind('<Button1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

        return self
    
