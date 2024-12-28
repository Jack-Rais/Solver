import tkinter as tk
from . import Mode



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

        self.open_pop_up()

        while self.last_capacity is None or self.last_id is None:
            self.canvas.winfo_toplevel().update()

        print(self.last_id)

        new_node = {
            'id': self.rect_id,
            'edges': [],
            'capacity': self.last_capacity,
            'nome_stanza': self.last_id,
            'type': 'node'
        }
        self.nodes.append(new_node)

        self.rect_id = None
        self.last_id = None


    def open_pop_up(self):

        popup = tk.Toplevel()
        popup.title("Capacità stanza massima")
        popup.geometry("300x200")

        label_id = tk.Label(popup, text="Inserisci l\'id della stanza, capacità massima della stanza:")
        label_id.grid(
            column = 0,
            row = 0
        )

        entry_id = tk.Entry(popup)
        entry_id.grid(
            column = 0,
            row = 1
        )

        label_capacity = tk.Label(popup, text="Inserisci la capacità massima della stanza:")
        label_capacity.grid(
            column = 0,
            row = 3
        )

        entry_capacity = tk.Entry(popup)
        entry_capacity.grid(
            column = 0,
            row = 4
        )

        error_label = tk.Label(popup, text="", fg="red")
        error_label.grid(
            column = 0,
            row = 5
        )

        def get_input():

            capacity = entry_capacity.get()
            id_stanza = entry_id.get()

            if capacity.isdigit():

                self.last_capacity = int(capacity)
                self.last_id = id_stanza
                popup.destroy()

            else:

                error_label.config(text="Per favore, inserisci valori validi")

        button = tk.Button(popup, text="Conferma", command=get_input)
        button.grid(
            column = 0,
            row = 6
        )

    
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

        self.last_capacity = None
        self.last_id = None

        self.canvas.bind('<Button-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_motion)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)

        return self