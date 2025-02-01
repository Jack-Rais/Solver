import tkinter as tk
import networkx as nx


class SubMode:

    def __init__(self, canvas:tk.Canvas, graph:nx.Graph, max_units:int, nodes:list):
        
        self.canvas = canvas
        self.graph = graph

        self.nodes = nodes
        
        self.max_units = max_units

        self.canvas.bind('<Button-1>', self.__on_touch)

    def search_node_by_pos(self, pos:tuple[int, int], 
                                 width_total:int = 600, 
                                 height_total:int = 500):
        
        xpos, ypos = pos
        
        for node in self.graph.nodes(data = True):

            node = node[1]['node']
            xstart, ystart, xend, yend = node.pos
            xstart, xend = xstart * width_total, xend * width_total
            ystart, yend = ystart * height_total, yend * height_total

            if xstart < xpos < xend and ystart < ypos < yend:
                return node
            
        return None

    def __on_touch(self, event:tk.Event):

        node = self.search_node_by_pos(
            (event.x, event.y), self.canvas.winfo_width(), self.canvas.winfo_height()
        )

        if node:
            node.units_count -= 1
            node.units_count = max(0, node.units_count)

            self.draw(node)

    def rgb_to_hex(self, r:int, g:int, b:int):
        return f"#{abs(r):02x}{abs(g):02x}{abs(b):02x}"
    

    def get_id_by_node(self, node):
        
        for node_idx, idx in self.nodes:
            if node_idx.id == node.id:
                return idx


    def draw(self, node):
        
        color = int(255 * (getattr(node, 'units_count') / self.max_units))
        node = self.get_id_by_node(node)

        self.canvas.itemconfig(
            node,
            fill = self.rgb_to_hex(255 - color, 255 - color, 255 - color)
        )

    def unbind(self):
        self.canvas.unbind('<Button-1>')