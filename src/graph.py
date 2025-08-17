import numpy as np
from numpy import random

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = np.array(vertices)
        self.edges = np.array([sorted(e) for e in edges]) # edges should always remain sorted

    def __str__(self):
        str = "\nGraph\n"
        str += f'  Vertices: {self.vertices.tolist()}\n'
        str += f'  Edges: {self.edges.tolist()}\n'
        return str

    def check_edges_sorted(self):
        if not np.all(self.edges[:, 0] <= self.edges[:, 1]):
            raise Exception(f"Error: Found unsorted edges in {self.edges}")
        
    def add_vertex(self, connecting_vertex_index, new_vertex):
        self.vertices = np.append(self.vertices, [new_vertex], axis=0)

        # add edge to connect vertices
        new_edge = (connecting_vertex_index, len(self.vertices)-1)
        self.edges = np.append(self.edges, [new_edge], axis=0)

    # can only remove vertex, if it's not connected to any other vertices
    def try_remove_vertex(self, vertex_index):

        connected_to_other = np.any(self.edges == vertex_index)
        if connected_to_other:
            return False

        # possible speed up: use np methods instead of for loop
        for i in range(len(self.edges)):
            # correct edges
            if self.edges[i][0] > vertex_index:
                self.edges[i][0] -= 1
            if self.edges[i][1] > vertex_index:
                self.edges[i][1] -= 1

        # remove vertex
        self.vertices = np.delete(self.vertices, [vertex_index], axis=0)

        return True


    def add_edge(self, edge):
        edge = sorted(edge)
        self.edges = np.append(self.edges, [edge], axis=0)

    def try_remove_edge(self, edge_index) -> bool:
        
        # possible speed up: I think creating new graph might cost significant memory
        temp_graph = Graph(self.vertices, self.edges)

        removing_edge = temp_graph.edges[edge_index]
        
        temp_graph.edges = np.delete(temp_graph.edges, [edge_index], axis=0)

        # if either vertex connected to edge has no other connections, remove it
        temp_graph.try_remove_vertex(removing_edge[0])
        temp_graph.try_remove_vertex(removing_edge[1])
        

        if self.is_connected():
            self.vertices = temp_graph.vertices.copy()
            self.edges = temp_graph.edges.copy()
            return True
        else:
            return False
    
    def is_connected(self):

        if len(self.edges) == 0:
            return False

        remaining_edges = self.edges.copy()
        def find_connections_r(edge_index):
            nonlocal remaining_edges

            edge = remaining_edges[edge_index]
            remaining_edges = np.delete(remaining_edges, [edge_index], axis=0)

            for edge_value in edge:
                rows, cols = np.where(remaining_edges == edge_value)

                no_connections = len(rows) == 0
                if no_connections:
                    continue

                connected_edge_index = rows[0]
                find_connections_r(connected_edge_index)

        find_connections_r(0)

        return len(remaining_edges) == 0

        
