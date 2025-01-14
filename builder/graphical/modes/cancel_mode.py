import tkinter as tk

from .base_mode import Mode


class CancelMode(Mode):


    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.canvas.bind('<Button-1>', self.on_mouse_press)


    def on_mouse_press(self, event: tk.Event):
        """Gestisce il click del mouse per cancellare il rettangolo selezionato."""

        for rect in self.nodes:

            rect_id = rect.get("id")
            coords = self.canvas.coords(rect_id)
            x1, y1, x2, y2 = coords

            # Verifica se il punto cliccato è all'interno del rettangolo
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:

                # Elimina il rettangolo dalla canvas
                self.canvas.delete(rect_id)
                self.nodes.remove(rect)

                # Rimuovi le linee (edges) collegate al nodo
                nodes_edges = [other_id for other_id, _, _ in rect['edges']]
                to_remove = [(rect_id, line_id) for _, line_id, _ in rect['edges']]

                # Rimuove i nodi che sono collegati
                for node_edge in [x for x in self.nodes if x['id'] in nodes_edges]:
                    for x in to_remove:

                        try:
                            node_edge['edges'].remove(x)

                        except ValueError:
                            pass

                for _, line_id in to_remove:
                    self.canvas.delete(line_id)

                break  # Interrompe il ciclo quando il nodo viene trovato e rimosso

    
    def unbind(self):

        self.canvas.unbind('<Button-1>')

    def pass_args(self):
        
        return {
            'canvas': self.canvas,
            'nodes': self.nodes,
            'background': self.background
        }