import networkx as nx
import pygame
import math
import sys

class City:


    def __init__(self):

        self.graph = nx.Graph()
        self.setup_called = False

    
    def setup_window(self, height:int,
                           width:int,
                           radius_nodes:int = 10,
                           width_nodes:int = 2,
                           width_edges:int = 3,
                           background_color:tuple = (0, 0, 0),
                           nodes_color:tuple = (0, 255, 0),
                           nodes_second:tuple = (0, 0, 255),
                           nodes_third:tuple = (0, 255, 255),
                           edges_color:tuple = (255, 0, 0),
                           edges_second:tuple = (255, 255, 0)):
        
        self.radius_nodes = radius_nodes
        self.width_nodes = width_nodes
        self.width_edges = width_edges
        
        self.last_clicked = None
        self.node_solution = []
        self.solution = []

        self.background_color = background_color
        self.nodes_color = nodes_color
        self.nodes_second = nodes_second
        self.nodes_third = nodes_third
        self.edges_color = edges_color
        self.edges_second = edges_second

        self.zoom = 1
        self.pan_x = 0
        self.pan_y = 0

        self.zoom_max = 3.0
        self.zoom_min = 0.2

        self.zoom_increase = 0.5
        self.zoom_decrease = 0.5

        self.movement_increase = 0.6

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.background_color)

        self.canvas = pygame.surface.Surface((width, height))
        self.canvas.fill(self.background_color)

        self.setup_called = True

    
    def check_if_stopped(self, events):

        if any([e.type == pygame.QUIT for e in events]):
            pygame.quit()
            sys.exit()


    def run(self):

        if not self.setup_called:
            raise KeyError("Before calling run you have to call setup_window()")
        
        clicking = False
        motion = False
        last_clicked_in = True
        removed = False

        while True:
            events = pygame.event.get()
            self.check_if_stopped(events)


            for click in [e for e in events if e.type == pygame.MOUSEBUTTONDOWN]:

                if click.button == 1:
                    
                    clicking = True
                    motion = False
                    last_clicked_in = self.is_click_in(click.pos)[0]


            for click in  [e for e in events if e.type == pygame.MOUSEMOTION]:

                if pygame.mouse.get_pressed()[0] and last_clicked_in and not motion:
                    self.last_clicked = self.is_click_in(click.pos)[1] or self.last_clicked

                motion = True

                if pygame.mouse.get_pressed()[0] and not last_clicked_in:

                    node = self.is_click_in(click.pos)

                    if node[0]:

                        self.canvas.fill(self.background_color)
                        self.graph.remove_node(node[1][0])
                        self.plot()

                        removed = True
                

            for click in [e for e in events if e.type == pygame.MOUSEBUTTONUP]:

                if not removed and click.button == 1:

                    node = self.is_click_in(click.pos)

                    if not node[0]:

                        self.create_node(click.pos)

                        if self.last_clicked is not None and motion and clicking:

                            node = self.is_click_in(click.pos)[1]
                            self.add_edge(node[0], self.last_clicked[0])

                            self.last_clicked = None

                        self.canvas.fill(self.background_color)
                        self.plot()

                    elif motion:
                        
                        self.canvas.fill(self.background_color)
                        self.add_edge(self.last_clicked[0], node[1][0])
                        self.plot()

                    else:

                        if self.graph.number_of_nodes() == 1:
                            print('You can\'t select a node if there aren\'t any others')

                        else:

                            self.click_node(node[1])
                            self.canvas.fill(self.background_color)
                            self.plot()
                    
                    clicking = False
                    motion = False
                
                if click.button == 1:
                    removed = False

                if click.button == 3:

                    node = self.is_click_in(click.pos)


                    if self.node_solution == [] and node[0]:
                        node[1][1]['surface'] = self.draw_node(3)
                        self.node_solution = node[1][0]
                        self.plot()

                    elif node[1][0] == self.node_solution:
                        self.node_solution = None
                        node[1][1]['surface'] = self.draw_node(3)
                        self.plot()

                    elif node[0]:

                        self.solution = nx.shortest_path(
                            self.graph,
                            self.node_solution,
                            node[1][0]
                        )
                        node[1][1]['surface'] = self.draw_node(3)

                        self.plot()

            
            self.update_zoom(events)
            self.transform()

            pygame.display.flip()

    
    def add_edge(self, node1, node2):
        
        point1 = self.graph.nodes[node1]['position']
        point2 = self.graph.nodes[node2]['position']

        intersections = []
        for edge in self.graph.edges:

            point3 = self.graph.nodes[edge[0]]['position']
            point4 = self.graph.nodes[edge[1]]['position']

            intersec = self.intersecting_segments(
                point1,
                point2,
                point3,
                point4
            )

            if intersec:
                intersections.append((intersec, edge))

        if not intersections:
            self.graph.add_edge(node1, node2)
            return
        
        intersections.sort(key=lambda x: ((x[0][0] - point1[0])**2 + (x[0][1] - point1[1])**2)**0.5)

        new_nodes = []
        for inter, edge in intersections:

            inter_node = self.create_node(inter)
            new_nodes.append(inter_node)

            other_node1, other_node2 = edge
            self.graph.remove_edge(other_node1, other_node2)
            self.graph.add_edge(other_node1, inter_node)
            self.graph.add_edge(inter_node, other_node2)

        all_nodes = [node1] + new_nodes + [node2]
        for i in range(len(all_nodes) - 1):
            self.graph.add_edge(all_nodes[i], all_nodes[i + 1])



    def intersecting_segments(self, p1, p2, p3, p4):

        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        x4, y4 = p4

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / den

        if 0 <= t <= 1 and 0 <= u <= 1:

            inter_x = x1 + t * (x2 - x1)
            inter_y = y1 + t * (y2 - y1)
            return (inter_x, inter_y)
        
        return None


    def update_zoom(self, events):
        
        for click in [e for e in events if e.type == pygame.MOUSEBUTTONDOWN]:

            if click.button == 4:
                self.zoom = min(self.zoom + self.zoom_increase, self.zoom_max)

            if click.button == 5:
                self.zoom = max(self.zoom - self.zoom_decrease, self.zoom_min)

        keys =  pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.pan_x -= self.movement_increase * self.zoom

        if keys[pygame.K_RIGHT]:
            self.pan_x += self.movement_increase * self.zoom

        if keys[pygame.K_UP]:
            self.pan_y -= self.movement_increase * self.zoom

        if keys[pygame.K_DOWN]:
            self.pan_y += self.movement_increase * self.zoom

        if keys[pygame.K_0]:
            self.zoom = 1
            self.pan_x = 0
            self.pan_y = 0


    def transform(self):
        
        scaled_canvas = pygame.transform.scale(
            self.canvas, 
            (int(self.canvas.get_width() * self.zoom), int(self.canvas.get_height() * self.zoom))
        )

        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_canvas, (-self.pan_x, -self.pan_y))
    
    
    def create_node(self, position):

        self.graph.add_node(
            int(str(int(position[0])) + str(int(position[1]))), 
            position = position,
            surface = self.draw_node()
        )

        for edge in [edge for edge in self.graph.edges if edge[1] != edge[0]]:

            node1 = self.graph.nodes[edge[0]]
            node2 = self.graph.nodes[edge[1]]

            x1, y1 = node1['position']
            x2, y2 = node2['position']

            xc, yc = position

            if self.intersecting_circle(x1, y1, x2, y2, xc, yc, self.radius_nodes):

                self.graph.remove_edge(edge[0], edge[1])

                self.graph.add_edge(edge[0], int(str(int(position[0])) + str(int(position[1]))))
                self.graph.add_edge(int(str(int(position[0])) + str(int(position[1]))), edge[1])

        return int(str(int(position[0])) + str(int(position[1])))

    
    def click_node(self, node):

        if self.last_clicked is not None and \
            node != self.last_clicked:

            self.add_edge(self.last_clicked[0], node[0])

            self.last_clicked[1]['surface'] = self.draw_node()
            self.last_clicked = None

        elif self.last_clicked is not None:

            self.last_clicked[1]['surface'] = self.draw_node()
            self.last_clicked = None

        else:
            node[1]['surface'] = self.draw_node(primary = 2)
            self.last_clicked = node


    
    def draw_node(self, primary = 1):

        circle_surface = pygame.surface.Surface(
            (self.radius_nodes * 2, self.radius_nodes * 2),
            flags = pygame.SRCALPHA
        )

        circle_surface.fill((0, 0, 0, 0))

        color = self.nodes_color if primary == 1 else \
                    self.nodes_second if primary == 2 else \
                        self.nodes_third

        pygame.draw.circle(
            circle_surface,
            color,
            (self.radius_nodes, self.radius_nodes),
            self.radius_nodes,
            width = self.width_nodes
        )

        return circle_surface


    
    def intersecting_circle(self, x1, y1, x2, y2, xc, yc, r):

        A = (x2 - x1) ** 2 + (y2 - y1) ** 2
        B = 2 * ((x2 - x1) * (x1 - xc) + (y2 - y1) * (y1 - yc))
        C = (x1 - xc) ** 2 + (y1 - yc) ** 2 - r ** 2
 
        delta = B ** 2 - 4 * A * C
        
        if delta < 0: 
            return False
        
        elif delta == 0:

            t = -B / (2 * A)
            return 0 <= t <= 1
        
        else:

            sqrt_delta = math.sqrt(delta)
            t1 = (-B - sqrt_delta) / (2 * A)
            t2 = (-B + sqrt_delta) / (2 * A)

            return (0 <= t1 <= 1) or (0 <= t2 <= 1)


    
    def is_click_in(self, position):

        for node in self.graph.nodes(data = True):

            x, y = node[1]['position']
            if math.sqrt((x - position[0]) ** 2 + (y - position[1]) ** 2) <= self.radius_nodes:
                return (True, node)
    
        return (False, None)
    


    def plot(self):

        for edge in [e for e in self.graph.edges() if e[0] != e[1]]:

            node1 = self.graph.nodes[edge[0]]
            node2 = self.graph.nodes[edge[1]]

            self.draw_line(node1, node2)

        for node in self.graph.nodes(data = True):
            
            x, y = node[1]['position']
            pos = x - self.radius_nodes, y - self.radius_nodes

            self.canvas.blit(node[1]['surface'], pos)


        self.plot_solution()

        

    def plot_solution(self):

        node_results = [
            self.graph.nodes(node) for node in self.solution if self.graph.has_node(node)
        ]

        if not len(node_results) == len(self.solution):
            self.solution = []

        solution = zip(self.solution[:-1], self.solution[1:])

        for node1, node2 in solution:

            self.draw_line(
                self.graph.nodes[node1], 
                self.graph.nodes[node2],
                primary = 2
            )



    def draw_line(self, node1, node2, primary = 1):

        x1, y1 = node1['position']
        x2, y2 = node2['position']
        
        diff_x = abs(x1 - x2)
        diff_y = abs(y1 - y2)

        ip = math.sqrt(diff_x ** 2 + diff_y ** 2)

        sin1 = diff_y / ip
        cos1 = diff_x / ip

        sin2 = diff_x / ip
        cos2 = diff_y / ip

        new_x1 = x1 + (-1 if x2 < x1 else 1) * self.radius_nodes * cos1
        new_y1 = y1 + (-1 if y2 < y1 else 1) * self.radius_nodes * sin1

        new_x2 = x2 + (-1 if x1 < x2 else 1) * self.radius_nodes * sin2
        new_y2 = y2 + (-1 if y1 < y2 else 1) * self.radius_nodes * cos2

        point1 = new_x1, new_y1
        point2 = new_x2, new_y2

        pygame.draw.line(
            self.canvas, 
            self.edges_color if primary == 1 else self.edges_second, 
            point1, 
            point2, 
            width = self.width_edges
        )


city = City()
city.setup_window(
    500,
    600
)

city.run()