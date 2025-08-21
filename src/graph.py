import numpy as np
from numpy import random

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = np.array(vertices)
        self.edges = np.array([sorted(e) for e in edges]) # edges should always remain sorted

    def __str__(self):
        str = "Graph\n"
        str += f'  Vertices: {self.vertices.tolist()}\n'
        str += f'  Edges: {self.edges.tolist()}'
        return str

    def check_edges_sorted(self):
        if not np.all(self.edges[:, 0] <= self.edges[:, 1]):
            raise Exception(f"Error: Found unsorted edges in {self.edges}")
        
    def add_vertex(self, connecting_vertex_index, new_vertex):

        if connecting_vertex_index >= len(self.vertices):
            raise Exception(f"Error: Trying to add vertex but connecting vertex index is out of range. \
                            Index: {connecting_vertex_index}, Graph: {self}")

        self.vertices = np.append(self.vertices, [new_vertex], axis=0)

        # add edge to connect vertices
        new_edge = (connecting_vertex_index, len(self.vertices)-1)
        self.edges = np.append(self.edges, [new_edge], axis=0)

    # can only remove vertex, if it's not connected to any other vertices
    def try_remove_vertex(self, vertex_index):

        if vertex_index >= len(self.vertices):
            raise Exception(f"Error: Trying to remove vertex but index {vertex_index} is out of range. Graph: {self}")

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

        if edge[0] >= len(self.vertices) or edge[1] >= len(self.vertices):
            raise Exception(f"Error: Trying to add edge {edge} to {self} At least one of the edge values is out of range.")

        edge = sorted(edge)

        if np.all(self.edges == edge, axis=1).any():
            print(f"Warning: Trying to add edge {edge} to {self} Graph already contains edge.")
            return

        self.edges = np.append(self.edges, [edge], axis=0)

    def try_remove_edge(self, edge_index) -> bool:

        if edge_index >= len(self.edges):
            raise Exception(f"Error: Trying to remove edge but index {edge_index} is out of range. Graph: {self}")

        # possible speed up: I think creating new graph might cost significant memory
        temp_graph = Graph(self.vertices, self.edges)

        removing_edge = temp_graph.edges[edge_index]
        
        temp_graph.edges = np.delete(temp_graph.edges, [edge_index], axis=0)

        # if either vertex connected to edge has no other connections, remove it
        # need to remove greater edge value (1) first because removing lower index first decreases
        # the index of each item after it by one.
        temp_graph.try_remove_vertex(removing_edge[1])
        temp_graph.try_remove_vertex(removing_edge[0])

        if temp_graph.is_connected():
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
    

    # make the min vertex positions 0, adjust all other vertex positions to keep same relative positions
    def normalize_vertices(self):
        xmin = self.vertices[:, 0].min()
        self.vertices[:, 0] = self.vertices[:, 0] - xmin

        ymin = self.vertices[:, 1].min()
        self.vertices[:, 1] = self.vertices[:, 1] - ymin

    def check_edges_sorted(self):
        if not np.all(self.edges[:, 0] <= self.edges[:, 1]):
            raise Exception(f"Error: Found unsorted edges in {self}")

    def get_edge_positions(self):
        edge_positions = [(self.vertices[pos1].copy(), self.vertices[pos2].copy()) for (pos1, pos2) in self.edges]
        return edge_positions
    
    def get_edge_pos(self, edge_index) -> np.array:
        edge = self.edges[int(edge_index)]
        return np.array((self.vertices[edge[0]].copy(), self.vertices[edge[1]].copy()))
    
    def get_edge_center(self, edge_index) -> np.array:
        pos1, pos2 = self.get_edge_pos((edge_index))
        center = (pos1 + pos2) / 2
        return center