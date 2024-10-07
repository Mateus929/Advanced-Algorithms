import numpy as np


class Graph:
    def __init__(self, matrix=None):
        self.number_of_nodes = 0
        self.nodes = {}  # Maps node values to their indices
        self.edges = []  # List of edges as tuples
        self.neighbours = {}  # Dictionary to store neighbours of each node
        self.locked = False  # Lock flag to prevent modifications

        if matrix is not None:
            self._initialize_from_matrix(matrix)

    def _initialize_from_matrix(self, matrix):
        """
        Initialize the graph from a given adjacency matrix.
        """
        self.number_of_nodes = matrix.shape[0]
        self.nodes = {i: i for i in range(self.number_of_nodes)}  # Map integers to themselves
        self.neighbours = {i: [] for i in range(self.number_of_nodes)}  # Initialize neighbours for each node

        for i in range(self.number_of_nodes):
            for j in range(self.number_of_nodes):
                if matrix[i, j] == 1:  # There is an edge from i to j
                    self.add_edge(i, j)

    def lock(self):
        """
        Lock the graph to prevent further modifications.
        """
        self.locked = True

    def add_node(self):
        """
        Add a new node to the graph and return its index.
        """
        if self.locked:
            raise Exception("Graph is locked. Cannot add nodes.")

        node_index = self.number_of_nodes
        self.nodes[node_index] = node_index
        self.neighbours[node_index] = []
        self.number_of_nodes += 1
        return node_index

    def add_edge(self, x, y):
        """
        Add an edge from node x to node y.
        If x or y are not mapped, map them by adding new nodes.
        """
        if self.locked:
            raise Exception("Graph is locked. Cannot add edges.")

        if x not in self.nodes:
            self.add_node()
        if y not in self.nodes:
            self.add_node()

        # Store the edge as a tuple
        self.edges.append((x, y))
        # Update the neighbours list
        self.neighbours[self.nodes[x]].append(self.nodes[y])

    def get_nodes(self):
        return self.nodes.values()

    def get_neighbors(self, v):
        """
        Return the list of neighbours for the vertex v.
        """
        if v in self.neighbours:
            return self.neighbours[v]
        else:
            return None

    def get_neighbors_iterator(self, v):
        """
        Return an iterator for the neighbours of vertex v.
        """
        if v in self.neighbours:
            return iter(self.neighbours[v])
        else:
            return iter([])  # Empty iterator if v has no neighbours

    def get_matrix(self):
        """
        Return an adjacency matrix representation of the graph.
        Returns 1 in i, j if (x, y) is an edge, zero otherwise.
        """
        matrix = np.zeros((self.number_of_nodes, self.number_of_nodes), dtype=int)

        for x, y in self.edges:
            i = self.nodes[x]  # Index for x
            j = self.nodes[y]  # Index for y
            matrix[i, j] = 1

        return matrix

    def visualize(self, path: str = "graph.jpg") -> None:
        """
        Tool for seeing graph visually.
        Gets and argument in format path/name.jpg and saves a jpg picture on that path.
        """
        import matplotlib.pyplot as plt
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from(self.edges)
        nx.draw(G, with_labels=True)
        plt.savefig(path, format="jpg")


# Example Usage
if __name__ == "__main__":
    # Create a graph from an adjacency matrix
    adjacency_matrix = np.array([[0, 1, 0],
                                 [0, 0, 1],
                                 [1, 0, 0]])

    graph = Graph(adjacency_matrix)

    print("Number of nodes:", graph.number_of_nodes)
    print("Nodes mapping:", graph.nodes)
    print("Edges:", graph.edges)
    print("Adjacency Matrix:")
    print(graph.get_matrix())

    # Lock the graph
    graph.lock()

    # Attempt to add a new node and edge (this will raise an exception)
    try:
        new_node = graph.add_node()
        graph.add_edge(2, new_node)
    except Exception as e:
        print("\nError:", e)

    # Get neighbours of a vertex
    vertex = 2
    print(f"\nNeighbours of vertex {vertex}:", graph.get_neighbors(vertex))

    # Iterate through neighbours of vertex
    print(f"Iterating through neighbours of vertex {vertex}:")
    neighbours_iterator = graph.get_neighbors_iterator(vertex)
    for neighbour in neighbours_iterator:
        print(neighbour)

    graph.visualize()
