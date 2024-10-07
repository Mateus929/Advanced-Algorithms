import collections

import numpy as np

from graph import Graph


class BipartiteGraph(Graph):

    def __init__(self, matrix=None):
        self.left_set = []
        self.right_set = []
        super().__init__(matrix)

    def lock(self):
        """
        Locks graph only if it is bipartite
        """
        if not self._check_for_bipartite():
            raise Exception("graph is not bipartite, hence cannot be locked")
        super().lock()

    def _check_for_bipartite(self):
        color = {}
        for node in self.get_nodes():
            if node not in color:
                if not self._bfs_check(node, color):
                    return False
        for node in self.get_nodes():
            if color[node] == 1:
                self.nodes[node] = (1, len(self.left_set))
                self.left_set.append(node)
            else:
                self.nodes[node] = (0, len(self.right_set))
                self.right_set.append(node)
        return True

    def _bfs_check(self, start_node, color):
        queue = collections.deque([start_node])
        color[start_node] = 0

        while queue:
            node = queue.popleft()
            for neighbor in self.get_neighbors(node):
                if neighbor not in color:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False  # Not bipartite
        return True

    def get_left_set(self):
        if self.locked:
            return self.left_set
        raise Exception("Graph isn't locked")

    def get_right_set(self):
        if self.locked:
            return self.right_set
        raise Exception("Graph isn't locked")

    def get_matrix(self, type="bipartite"):

        if not type in ["adjacency", "bipartite"]:
            raise Exception("Type must be either adjacency or bipartite")

        if type == "adjacency" or not self.locked:
            return super().get_matrix()

        matrix = np.zeros((len(self.left_set), len(self.right_set)), dtype=int)

        for x, y in self.edges:
            cli, i = self.nodes[x]
            clj, j = self.nodes[y]
            if cli == 1:
                i, j = j, i
            matrix[i, j] = 1
        return matrix

    def visualize(self, path: str = "graph.jpg") -> None:
        if self.locked:
            import matplotlib.pyplot as plt
            import networkx as nx
            G = nx.Graph()
            G.add_edges_from(self.edges)
            nx.draw(G, self.nodes, with_labels=True,
                    node_color=['lightblue' if node in self.left_set else 'lightgreen' for node in G.nodes()],
                    node_size=500)
            plt.savefig(path, format="jpg")
            print("here")
        else:
            super().visualize()


# Example Usage
if __name__ == "__main__":
    # Create a graph from an adjacency matrix
    adjacency_matrix = np.array([[0, 0, 1, 1],
                                 [0, 0, 1, 1],
                                 [1, 1, 0, 0],
                                 [1, 1, 0, 0]])

    graph = BipartiteGraph(adjacency_matrix)

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

    print(graph.get_matrix())

    graph.visualize()