"""
Finds shortest path from a source vertex s to every other vertex in an undirected graph
"""

from graph_api import Graph
from collections import deque


class BreadthFirstPaths(object):

    def __init__(self, graph_obj, src):
        if graph_obj is None or src < 0:
            raise ValueError("Graph object cannot be None. src should be a hashed non-negative "
                             "integer < number of vertices in graph")
        self._marked = [False] * graph_obj.v()
        self._dist_to = [float('inf')] * graph_obj.v()
        self._edge_to = [None] * graph_obj.v()  # edge_to[v] = last edge on the src to v path
        self.bfs(graph_obj, src)

    def bfs(self, graph_obj, src):
        """
        Time complexity is O(V + E)
        breadth-first search from single source to find the shortest path from src to each node
        Biggest application of breadth-first-search is Dijkstra's shortest path.
        Shortest path is the theme of 70% of graph interviews.

        Dijkstra's shortest path algorithm works with cycles and works for directed graphs.
        It doesn't work only for negative-weighted edges
        :param graph_obj:
        :param src:
        :return:
        """
        self._dist_to[src] = 0
        self._marked[src] = True
        q = deque()
        q.append(src)
        while q:
            v = q.pop()
            for u in graph_obj.adj(v):
                if not self._marked[u]:
                    self._dist_to[u] = self._dist_to[v] + 1
                    self._edge_to[u] = v
                    self._marked[u] = True
                    q.append(u)

if __name__ == '__main__':
    l = [13, 13, (0, 5), (4,3), (0,1), (9, 12), (6,4), (5,4), (0,2), (11, 12), (9, 10), (0,6),
         (7,8), (9,11), (5,3)]
    g = Graph(l)
    bfp = BreadthFirstPaths(g, 6)
    print bfp._edge_to  # [6, 0, 0, 4, 6, 4, None, None, None, None, None, None, None]
    print bfp._marked  # [True, True, True, True, True, True, True, False, False, False, False,
    # False, False]
    print bfp._dist_to  # [1, 2, 2, 2, 1, 2, 0, inf, inf, inf, inf, inf, inf]
    # shortest path array from src 6
