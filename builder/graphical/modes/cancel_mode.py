import tkinter as tk

from .base_mode import Mode
from ...network.bases import Node


class CancelMode(Mode):


    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.canvas.bind('<Button-1>', self.on_mouse_press)


    def on_mouse_press(self, event: tk.Event):
        """Gestisce il click del mouse per cancellare il rettangolo selezionato."""

        for rect in self.nodes:

            rect:Node = rect

            rect_id = rect.id
            coords = self.canvas.coords(rect_id)
            x1, y1, x2, y2 = coords

            # Verifica se il punto cliccato è all'interno del rettangolo
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:

                # Elimina il rettangolo dalla canvas
                self.canvas.delete(rect_id)
                self.nodes.remove(rect)

                for edge in rect.edges.list_edges:
                    
                    other_node = self.nodes.get_node(edge.other_id)
                    other_node.remove_edge(rect.id)

                    self.canvas.delete(edge.line_id)

                break  # Interrompe il ciclo quando il nodo viene trovato e rimosso

    
    def unbind(self):

        self.canvas.unbind('<Button-1>')

    def pass_args(self):
        
        return {
            'canvas': self.canvas,
            'nodes': self.nodes,
            'background': self.background
        }