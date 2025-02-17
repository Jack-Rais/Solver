import networkx as nx
import math



class System:


    def __init__(self):
        pass

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
                

                contact_points = [(x1_max, overlap_min), (x1_max, overlap_max)] if x1_max < x2_min \
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

                contact_points = [(overlap_min, y1_max), (overlap_max, y1_max)] if y1_max < y2_min \
                    else [(overlap_min, y1_min), (overlap_max, y1_min)]
                

        # If no contact points were found
        if not contact_points:
            return False, [], None

        # Edge case: If both points are identical, there's no real contact
        if len(contact_points) == 2 and contact_points[0] == contact_points[1]:
            return False, [], None

        return True, tuple(contact_points), type_contact


    def __create_middle_nodes(self, graph:nx.Graph) -> nx.Graph:

        new_graph = nx.Graph()

        for edge in graph.edges():


            xstart1, ystart1, xend1, yend1 = graph.nodes[edge[0]]['node'].pos
            xstart2, ystart2, xend2, yend2 = graph.nodes[edge[1]]['node'].pos


            is_there, contact, type_contact = self.__get_adjacency(
                ((xstart1, ystart1), (xend1, yend1)),
                ((xstart2, ystart2), (xend2, yend2)),
                allow_distance = True
            )

            (x1, y1), (x2, y2) = contact
            x_pos = (x1 + x2) / 2
            y_pos = (y1 + y2) / 2

            if not new_graph.has_node(str(edge[0]) + '-' + str(edge[1])):

                new_graph.add_node(
                    str(edge[0]) + '-' + str(edge[1]),
                    center = (x_pos, y_pos),
                    units_count = 0
                )


            if not new_graph.has_node(str(edge[0])):

                new_graph.add_node(
                    str(edge[0]),
                    center = ((xstart1 + xend1) / 2, (ystart1 + yend1) / 2),
                    units_count = graph.nodes[edge[0]]['node'].units_count
                )


            if not new_graph.has_node(str(edge[1])):

                new_graph.add_node(
                    str(edge[1]),
                    center = ((xstart2 + xend2) / 2, (ystart2 + yend2) / 2),
                    units_count = graph.nodes[edge[1]]['node'].units_count
                )


            new_graph.add_edge(str(edge[0]), str(edge[0]) + '-' + str(edge[1]))
            new_graph.add_edge(str(edge[1]), str(edge[0]) + '-' + str(edge[1]))


        return new_graph


    def normalize_v1_graph(self, graph:nx.Graph):

        new_graph = self.__create_middle_nodes(graph)
        end_graph = nx.Graph()

        for node in new_graph.nodes(data = True):
            end_graph.add_node(node[0], **node[1])

            for edge in new_graph.edges(node[0]):
                
                other_edge = edge[0] if edge[1] == node[0] else edge[1]

                if len(list(x := new_graph.edges(other_edge))) <= 2:
                    
                    for u, v in x:
                        end_graph.add_edge(
                            u, v,
                            weight = math.sqrt(
                                    (
                                        new_graph.nodes[u]['center'][0] + \
                                        new_graph.nodes[v]['center'][0]
                                    ) ** 2 + (
                                        new_graph.nodes[u]['center'][1] + \
                                        new_graph.nodes[v]['center'][1]
                                    ) ** 2
                                )
                        )

                else:
                    
                    for edge_other in x:

                        other_edge_other = edge_other[0] if edge_other[1] == other_edge else edge_other[1]

                        if not end_graph.has_edge(other_edge, other_edge_other):
                            end_graph.add_edge(
                                other_edge, other_edge_other,
                                weight = math.sqrt(
                                    (
                                        new_graph.nodes[other_edge]['center'][0] + \
                                        new_graph.nodes[other_edge_other]['center'][0]
                                    ) ** 2 + (
                                        new_graph.nodes[other_edge]['center'][1] + \
                                        new_graph.nodes[other_edge_other]['center'][1]
                                    ) ** 2
                                )
                            )

                        if not end_graph.has_edge(node[0], other_edge_other):
                            end_graph.add_edge(
                                node[0], other_edge_other,
                                weight = math.sqrt(
                                    (
                                        new_graph.nodes[node[0]]['center'][0] + \
                                        new_graph.nodes[other_edge_other]['center'][0]
                                    ) ** 2 + (
                                        new_graph.nodes[node[0]]['center'][1] + \
                                        new_graph.nodes[other_edge_other]['center'][1]
                                    ) ** 2
                                )
                            )


        return end_graph