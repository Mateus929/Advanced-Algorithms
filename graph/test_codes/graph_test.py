import numpy as np
from graph.graph import Graph

def test_graph_initialization():
    adjacency_matrix = np.array([[0, 1, 0],
                                  [0, 0, 1],
                                  [1, 0, 0]])
    graph = Graph(adjacency_matrix)

    assert graph.number_of_nodes == 3
    assert graph.nodes == {0: 0, 1: 1, 2: 2}
    assert graph.edges == [(0, 1), (1, 2), (2, 0)]
    np.testing.assert_array_equal(graph.get_matrix(), adjacency_matrix)

def test_add_node():
    graph = Graph()
    new_node_index = graph.add_node()

    assert new_node_index == 0
    assert graph.number_of_nodes == 1
    assert graph.nodes == {0: 0}
    assert graph.neighbours[0] == []

def test_add_edge():
    graph = Graph()
    graph.add_node()  # Add node 0
    graph.add_node()  # Add node 1
    graph.add_edge(0, 1)

    assert graph.edges == [(0, 1)]
    assert graph.neighbours[0] == [1]

def test_get_neighbours():
    graph = Graph()
    graph.add_node()  # Node 0
    graph.add_node()  # Node 1
    graph.add_edge(0, 1)

    neighbours = graph.get_neighbours(0)
    assert neighbours == [1]

def test_get_neighbours_iterator():
    graph = Graph()
    graph.add_node()  # Node 0
    graph.add_node()  # Node 1
    graph.add_edge(0, 1)

    iterator = graph.get_neighbours_iterator(0)
    assert list(iterator) == [1]

def test_graph_after_adding_node_and_edge():
    adjacency_matrix = np.array([[0, 1, 0],
                                  [0, 0, 1],
                                  [1, 0, 0]])
    graph = Graph(adjacency_matrix)

    new_node = graph.add_node()
    graph.add_edge(2, new_node)

    assert graph.number_of_nodes == 4
    assert new_node in graph.nodes
    assert graph.edges == [(0, 1), (1, 2), (2, 0), (2, 3)]
    updated_matrix = graph.get_matrix()
    expected_matrix = np.array([[0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [1, 0, 0, 1],
                                 [0, 0, 0, 0]])  # Updated expected adjacency matrix
    np.testing.assert_array_equal(updated_matrix, expected_matrix)

