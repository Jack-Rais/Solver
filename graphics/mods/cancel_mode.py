import tkinter as tk
from . import Mode

from pprint import pprint


class CancelMode(Mode):

    def on_mouse_touch(self, event:tk.Event):

        for rect in self.nodes:

            rect_id = rect.get("id")
            coords = self.canvas.coords(rect_id)
            x1, y1, x2, y2 = coords

            if x1 <= event.x <= x2 and y1 <= event.y <= y2:

                self.canvas.delete(rect_id)
                self.nodes.remove(rect)

                nodes_edges = []
                to_remove = []
                for other_id, line_id in rect['edges']:
                    nodes_edges.append(other_id)
                    to_remove.append((rect_id, line_id))
                    self.canvas.delete(line_id)

                for node_edge in [x for x in self.nodes if x['id'] in nodes_edges]:

                    for x in to_remove:

                        try:
                            node_edge['edges'].remove(x)

                        except ValueError:
                            pass

                break

    def unbind(self):

        self.canvas.unbind('<Button-1>')


    def __call__(self, canvas:tk.Canvas,
                       nodes:list[dict] | None = None):
        
        self.canvas = canvas
        self.nodes = nodes if nodes else []

        self.canvas.bind('<Button-1>', self.on_mouse_touch)

        return self