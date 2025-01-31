import tkinter as tk
import networkx as nx


class AddMode:

    def __init__(self, canvas:tk.Canvas, graph:nx.Graph):
        
        self.canvas = canvas
        self.graph = graph

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
            node.units_count += 1
            node.units_count = min(node.capacity, node.units_count)

            print(node.id, node.units_count)

    def unbind(self):
        self.canvas.unbind('<Button-1>')