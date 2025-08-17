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
        for i in range(len(self.edges) - 1, 0, -1):
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

        print(f'temp_graph.vertices: {temp_graph.vertices}')
        print(f'removing_edge: {removing_edge}')

        # if either vertex connected to edge has no other connections, remove it
        if not np.any(temp_graph.edges == removing_edge[0]):
            print(f"try remove vertex {temp_graph.vertices[removing_edge[0]]}")
            self.try_remove_vertex(removing_edge[0])

        if not np.any(temp_graph.vertices == removing_edge[1]):
            print(f"try remove vertex {temp_graph.vertices[removing_edge[1]]}")
            self.try_remove_vertex(removing_edge[1])


        
        self.vertices = temp_graph.vertices.copy()
        self.edges = temp_graph.edges.copy()
        return True

        
