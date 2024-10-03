import collections
from .graph import Graph


class BipartiteGraph(Graph):

    def __init__(self):
        super().__init__()
        self.left_set = []
        self.right_set = []

    def lock(self):
        """
        Locks graph only if it is bipartite
        """
        if not self._check_for_bipartite():
            raise Exception("graph is not bipartite, hence cannot be locked")
        self.locked = True

    def _check_for_bipartite(self):
        color = {}
        for node in self.get_nodes():
            if node not in color:
                if not self._bfs_check(node, color):
                    return False
        for node in self.get_nodes():
            if color[node] == 1:
                self.left_set.append(node)
            else:
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
        return self.left_set

    def get_right_set(self):
        return self.right_set


