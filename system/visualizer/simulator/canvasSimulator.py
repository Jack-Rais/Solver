import tkinter as tk
import networkx as nx

from functools import partial
from itertools import chain

from .canvasVisual import CanvasVisualizer
import sys
import os

from ...solver import Solver
from ...solver.modifier import System

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "...")))
#from solver.modifier import System


class Simulator:

    def __init__(self, graph:nx.Graph, parent:tk.Tk, stat:str = 'units_count', max_units:int | None = None):
        
        self.graph = graph
        self.initial_graph = graph
        self.canvas_intern:CanvasVisualizer = CanvasVisualizer(parent, self.graph)

        self.max_units = max_units

        self.stat = stat
        self.set_graph(graph)


    def simulate(self):
        """
        Avvia il ciclo di aggiornamento usando il metodo after di tkinter.
        """

        total_path:tuple[float, dict[int, dict[int, int]]] = self.solver.solve()
        total_saved, self.path = total_path

        self.graph = self.solver.graph

        print(self.path)

        self.update_simulation()


    def simulate_path(self):

        """
        Disegna ogni percorso che il sistema ha calcolato
        """

        sis = System()

        graph = sis.normalize_v1_graph(self.graph)

        is_found, dict_paths, points = self.solver.solve_every_room(graph)
        cleaned_path = self.solver.clean_path(dict_paths)
        points_path = self.solver.clean_path_points(dict_paths, points)
        
        print(is_found)
        print(tuple(cleaned_path.items()))


        all_elements = self.canvas_intern.canvas.find_all()
        rect_elements = [
            element for element in all_elements if self.canvas_intern.canvas.type(element) == 'rectangle'
        ]

        for rect in rect_elements:

            node = self.canvas_intern.get_node_by_id_in(rect)
            if node.type != "safezone":

                self.canvas.itemconfig(
                    rect,
                    fill = "white"
                )

        
        # Trovare le stanze di cui non si è trovata un uscita
        full_rooms = []
        for room in graph.nodes(data = True):

            if room[1]['units_count'] > 0:
                full_rooms.append(room[0])


        found_rooms = [
                    y for y, x in cleaned_path.items()
                ]


        rooms = [
            node for node in (
                item for item in full_rooms if not item in found_rooms
            )
        ]


        for node in rooms:

            x, y = graph.nodes[node]['center']

            self.canvas.create_oval(
                x * self.canvas.winfo_width() - 5,
                y * self.canvas.winfo_height() - 5,
                x * self.canvas.winfo_width() + 5,
                y * self.canvas.winfo_height() + 5,
                fill = 'red',
                width = 3
            )


        

        self.update_path_simulation(
            tuple(points_path.items())
        )

    
    def update_path_simulation(self, points:tuple[int, tuple], num:int = 0):

        all_elements = self.canvas_intern.canvas.find_all()
        line_elements = [
            element for element in all_elements if self.canvas_intern.canvas.type(element) == 'line'
        ]

        for line in line_elements:
            self.canvas.delete(line)

        if len(points) <= num:
            self.set_graph(self.initial_graph)
            return
        
        idx, path = points[num]

        for n, center in enumerate(path):

            if n + 1 < len(path):

                x1, y1 = center[0] * self.canvas.winfo_width(), center[1] * self.canvas.winfo_height()
                x2, y2 = path[n + 1][0] * self.canvas.winfo_width(), path[n + 1][1] * self.canvas.winfo_height()

                '''self.canvas_intern.canvas.create_oval(
                    x1 - 5,
                    y1 - 5,
                    x1 + 5,
                    y1 + 5,
                    fill = 'black'
                )'''

                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill = 'red',
                    width = 3
                )

        
        self.canvas_intern.canvas.after(
            1000, 
            partial(self.update_path_simulation, points, num + 1)
        )


        
    

    def __get_adjacency(self, rect1, rect2, allow_distance):
        """
        Determines whether two rectangles are adjacent and, optionally, their proximity if not touching.

        Args:
            rect1 (Tuple[Tuple[int, int], Tuple[int, int]]): First rectangle ((x_min, y_min), (x_max, y_max)).
            rect2 (Tuple[Tuple[int, int], Tuple[int, int]]): Second rectangle ((x_min, y_min), (x_max, y_max)).
            allow_distance (bool): If True, considers proximity even when rectangles do not touch.

        Returns:
            Tuple:
                - bool: True if rectangles are adjacent or close (depending on `allow_distance`).
                - List[Tuple[int, int], Tuple[int, int]]: List of contact points (if any).
                - Optional[Literal['horizontal', 'vertical']]: Contact direction ('horizontal' or 'vertical'), None if no contact.
        """

        def normalize(rect):
            (x1, y1), (x2, y2) = rect
            return (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2))

        (x1_min, y1_min), (x1_max, y1_max) = normalize(rect1)
        (x2_min, y2_min), (x2_max, y2_max) = normalize(rect2)

        contact_points = []
        type_contact = None


        # Check horizontal overlap
        if y1_min < y2_max and y2_min < y1_max:  
            overlap_min, overlap_max = max(y1_min, y2_min), min(y1_max, y2_max)
            
            # If the two rectangles have a contact point
            if x1_max == x2_min or x1_min == x2_max:
                type_contact = 'horizontal'

                # Check if the contact point is on the left or the right
                if x1_max == x2_min:
                    contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)]

                elif x1_min == x2_max:
                    contact_points = [(x1_min, overlap_min), (x1_min, overlap_max)]

            # If the two rectangles are one under the other and the allow_distance is on
            elif allow_distance and overlap_min <= overlap_max:
                type_contact = 'horizontal'

                contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)] if x1_max == x2_min \
                    else [(x1_min, overlap_min), (x1_min, overlap_max)]


        # Check vertical overlap
        elif x1_min < x2_max and x2_min < x1_max:
            overlap_min, overlap_max = max(x1_min, x2_min), min(x1_max, x2_max)

            # If the two rectangles have a contact point
            if y1_max == y2_min or y1_min == y2_max:
                type_contact = 'vertical'

                # Check if the contact point is on the top or the bottom
                if y1_max == y2_min:
                    contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)]

                elif y1_min == y2_max:
                    contact_points = [(overlap_min, y1_min), (overlap_max, y1_min)]

            # If the two rectangles are one after the other and the allow_distance is on
            elif allow_distance and overlap_min <= overlap_max:
                type_contact = 'vertical'

                contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)] if y1_max == y2_min \
                    else [(overlap_min, y1_min), (overlap_max, y1_min)]
                

        # If no contact points were found
        if not contact_points:
            return False, [], None

        # Edge case: If both points are identical, there's no real contact
        if len(contact_points) == 2 and contact_points[0] == contact_points[1]:
            return False, [], None
        

        return True, tuple(contact_points), type_contact



    def draw_connection(self, node1, node2, type_connection = 'arrow'):
        """Disegna una connessione tra due nodi."""

        x1_1, y1_1, x2_1, y2_1 = self.canvas.coords(self.canvas_intern.get_id_by_node(node1))
        x1_2, y1_2, x2_2, y2_2 = self.canvas.coords(self.canvas_intern.get_id_by_node(node2))

        contact, where, type_contact = self.__get_adjacency(
            ((x1_1, y1_1), (x2_1, y2_1)),
            ((x1_2, y1_2), (x2_2, y2_2)),
            True
        )

        if not contact:
            return False

        (x1, y1), (x2, y2) = where
        x_pos = (x1 + x2) / 2
        y_pos = (y1 + y2) / 2


        if type_connection == 'line':

            x_pos1, y_pos1 = (x1_1 + x2_1) / 2, (y1_1 + y2_1) / 2
            x_pos2, y_pos2 = (x1_2 + x2_2) / 2, (y1_2 + y2_2) / 2

            if type_contact == 'vertical':
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

            id_line = self.canvas.create_line(*punti, width=2, fill='red')

        elif type_connection == 'arrow':

            if type_contact == 'vertical':

                height_node1 = abs(y1_1 - y1_2)
                height_node2 = abs(y2_1 - y2_2)

                len_line = int(min(height_node1, height_node2) * 0.2)

                id_line = self.canvas.create_line(
                    x_pos, 
                    y_pos - len_line, 
                    x_pos, 
                    y_pos + len_line, width=2, fill='red'
                )

            elif type_contact == 'horizontal':

                width_node1 = abs(x1_1 - x1_2)
                width_node2 = abs(x2_1 - x2_2)

                len_line = int(min(width_node1, width_node2) * 0.2)

                id_line = self.canvas.create_line(
                    x_pos - len_line,
                    y_pos, 
                    x_pos + len_line, 
                    y_pos, width=2, fill='red'
                )

            else:
                raise ValueError('type_contact must be only "vertical" or "horizontal"')
        
        return id_line




    
    def draw_new_edges(self, path:dict[int, dict]):

        for id_node, edges in path.items():
            for edge, _ in edges.items():

                node1 = self.graph.nodes[id_node]['node']
                node2 = self.graph.nodes[edge]['node']

                if node1.type != 'safezone' and node2.type != 'safezone':
                    self.draw_connection(node1, node2)

                else:
                    self.draw_connection(node1, node2, 'line')



    def update_simulation(self):
        """
        Esegue un passaggio della simulazione, aggiorna le posizioni e pianifica il prossimo aggiornamento.
        """

        all_elements = self.canvas_intern.canvas.find_all()
        line_elements = [
            element for element in all_elements if self.canvas_intern.canvas.type(element) == 'line'
        ]

        for line in line_elements:
            self.canvas.delete(line)

        
        # Aggiungi la funzione per disegnare delle piccole linee tra i nodi che sono usati al momento
        path = self.prepare_path(self.path)

        self.draw_new_edges(path)
        self.update_positions(path)

        self.draw()

        # Pianifica il prossimo aggiornamento
        if len(path) != 0:
            self.canvas_intern.canvas.after(1000, self.update_simulation)

        else:
            self.set_graph(self.initial_graph)

    
    def set_graph(self, graph: nx.Graph):

        self.graph = graph
        self.initial_graph = graph
        self.solver = Solver(self.graph)
        self.canvas_intern.set_graph(self.graph)

        if self.max_units is None:
            self.max_units = max(
                [
                    node[1]['node'].capacity for node in self.graph.nodes(data=True) \
                        if node[1]['node'].type != 'safezone'
                ]
            )
        self.draw()

            

    def rgb_to_hex(self, r:int, g:int, b:int):
        return f"#{abs(r):02x}{abs(g):02x}{abs(b):02x}"


    def update_counter(self, node):
        # Ottieni le coordinate del nodo
        x1, y1, x2, y2 = self.canvas_intern.canvas.coords(
            self.canvas_intern.get_id_by_node(node)
        )
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Se il testo esiste già, aggiornalo
        if hasattr(node, 'text_bg') and hasattr(node, 'text'):
            # Aggiorna il testo
            self.canvas_intern.canvas.itemconfig(
                node.text,
                text=f'Tot: {node.units_count}'
            )
        else:
            # Crea un rettangolo bianco come sfondo
            bg_id = self.canvas_intern.canvas.create_rectangle(
                center_x - 40, center_y - 15,
                center_x + 40, center_y + 15,
                fill='white',
                outline='black'
            )
            
            # Crea il testo sopra il rettangolo
            text_id = self.canvas_intern.canvas.create_text(
                center_x,
                center_y,
                text=f'Tot: {node.units_count}',
                font=("Arial", 12, "bold"),
                fill='black'
            )
            
            # Salva i riferimenti
            setattr(node, 'text_bg', bg_id)
            setattr(node, 'text', text_id)
        
        # Assicurati che sia visibile
        self.canvas_intern.canvas.tag_raise(node.text_bg)
        self.canvas_intern.canvas.tag_raise(node.text)
    
    def draw(self):

        for node in [node[1]['node'] for node in self.graph.nodes(data=True)]:

            if node.id not in ['super_supply', 'super_demand'] and node.type != "safezone":
                id_node = self.get_id_by_node(node)

                color = int(255 * (getattr(node, self.stat) / self.max_units))

                self.canvas_intern.canvas.itemconfig(
                    id_node,
                    fill = self.rgb_to_hex(255 - color, 255 - color, 255 - color)
                )

            else:

                id_node = self.get_id_by_node(node)
                self.canvas_intern.canvas.itemconfig(
                    id_node,
                    fill = self.rgb_to_hex(0, 0, 0)
                )


    def prepare_path(self, path:dict[int, dict[int, float]]):

        new_path = dict()
        for node_id, nodes_to in path.items():

            if node_id not in ['super_supply', 'super_demand']:
                node = self.graph.nodes[node_id]['node']

                if getattr(node, self.stat) > 0:
                    new_path[node_id] = {
                        other_id: min(
                            flow, getattr(node, self.stat), self.graph[node_id][other_id]['edge'].capacity
                        ) for other_id, flow in nodes_to.items() \
                            if not other_id in ['super_supply', 'super_demand']
                    }

        cleaned_path = dict()
        for node_id, nodes_to in new_path.items():

            for other_id, flow in nodes_to.items():
                
                if flow != 0:
                
                    if cleaned_path.get(node_id, None) is None:
                        cleaned_path[node_id] = {
                            other_id: flow
                        }

                    else:
                        cleaned_path[node_id][other_id] = flow

        return cleaned_path
    


    def update_positions(self, path: dict[str, dict]):
        """
        Aggiorna le posizioni dei nodi in base al percorso e al flusso calcolato.
        Restituisce un dizionario con le unità rimanenti per ogni nodo.
        """

        for id_room, to_rooms in path.items():
            current_node = self.graph.nodes[id_room]['node']  # Nodo sorgente

            for target_id, flow in to_rooms.items():
                target_node = self.graph.nodes[target_id]['node']

                print(f"From {current_node.id} ({current_node.units_count:.2f}) ", end='')
                print(f"to {target_node.id} ({target_node.units_count:.2f}) ", end='')
                print(f"{flow:.2f} units")

                current_node.units_count = max(0, current_node.units_count - flow)
                target_node.units_count = target_node.units_count + flow

        print('-' * 40)

    def get_id_by_node(self, node):
        return self.canvas_intern.get_id_by_node(node)
    

    @property
    def canvas(self):
        return self.canvas_intern.canvas
    
    

    def unbind(self):
        return