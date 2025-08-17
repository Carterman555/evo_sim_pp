import unittest, sys, os
import numpy as np

# so can import graph
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graph import Graph

class TestGraph(unittest.TestCase):

    def test_add_vertex1(self):
        vertices = [[0,0],[10,0],[0,10]]
        edges = [[0,1],[1,2],[2,0]]
        graph = Graph(vertices,edges)
        
        graph.add_vertex(2, [10,10])

        self.assertListEqual(graph.vertices.tolist(), [[0,0],[10,0],[0,10],[10,10]])
        self.assertListEqual(graph.edges.tolist(), [[0,1],[1,2],[0,2],[2,3]])

    def test_remove_vertex1(self):
        vertices = [[0,0],[10,0],[10,10],[0,10]]
        edges = [[0,1],[3,0]]
        graph = Graph(vertices,edges)

        could_remove = graph.try_remove_vertex(2)
        self.assertTrue(could_remove)

        self.assertListEqual(graph.vertices.tolist(), [[0,0],[10,0],[0,10]])
        self.assertListEqual(graph.edges.tolist(), [[0,1],[0,2]])

    def test_remove_vertex2(self):
        vertices = [[0,0],[10,0],[10,10],[0,10]]
        edges = [[0,1],[1,2],[2,3],[3,0]]
        graph = Graph(vertices,edges)

        could_remove = graph.try_remove_vertex(2)
        self.assertFalse(could_remove)

    def test_add_edge(self):
        vertices = [[0,0],[10,0],[10,10],[0,10]]
        edges = [[0,1],[1,2],[2,3],[3,0]]
        graph = Graph(vertices,edges)

        graph.add_edge([2,0])

        self.assertListEqual(graph.vertices.tolist(), [[0,0],[10,0],[10,10],[0,10]])
        self.assertListEqual(graph.edges.tolist(), [[0,1],[1,2],[2,3],[0,3],[0,2]])

    def test_remove_edge_partial(self):
        vertices = [[0,0],[10,0],[10,10],[0,10]]
        edges = [[0,1],[1,2],[2,3],[3,0]]
        graph = Graph(vertices,edges)

        could_remove1 = graph.try_remove_edge(0)
        could_remove2 = graph.try_remove_edge(1)

        self.assertTrue(could_remove1)
        self.assertTrue(could_remove2)

        self.assertListEqual(graph.vertices.tolist(), [[0,0],[10,10],[0,10]])
        self.assertListEqual(graph.edges.tolist(), [[1,2],[0,2]])