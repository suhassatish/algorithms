"""
Directed graph - implemented using an adjacency list. Parallel edges and self-loops are permitted
"""


class Digraph(object):
    def __init__(self, a):
        if isinstance(a, int):
            self._init_empty(a)
        elif isinstance(a, Digraph):
            self._init_from_graph(a)
        elif isinstance(a, list) and len(a) == 1:
            self._init_empty(a[0])
        elif isinstance(a, list):
            self._init(a)

    def _init_empty(self, num_vertices):
        if num_vertices < 0:
            raise Exception("Number of vertices must be non-negative")

        # this is an adjacency_list indexed by vertex
        # each indexed element is a set of nodes that are connected to this vertex
        self._adj = [set() for _ in xrange(num_vertices)]

        self._V = num_vertices
        self._E = 0

    def _init(self, input_stream_with_edges):
        """
        The format of input_stream_with_edges is a list.
        The number of vertices is lst[0], lst[1] = number_of_edges , lst[2:] = tuple of directed
        edges
        :param input_stream_with_edges:
        :return:
        """
        self._init_empty(input_stream_with_edges[0])
        self._E = 0
        for v,w in input_stream_with_edges[2:]:
            self.add_edge(v, w)

    def _init_from_graph(self, digraph_obj):
        """
        This deep copies the input graph_obj to create a cloned graph.
        Note the difference in implementation to undirected graph.
        :return:
        """
        self._init_empty(digraph_obj.v())
        self._E = digraph_obj.e()
        for v in xrange(digraph_obj.v()):

            # keep reverse stack so that adj_list is in same order as original
            rev_stk = []
            for w in digraph_obj.adj(v):
                rev_stk.append(w)

            for w in rev_stk.pop():
                self._adj[v].add(w)

    def add_edge(self, v, w):
        """
        Adds the directed edge v->w to Digraph
        :param v:
        :param w:
        :return:
        """
        self._adj[v].add(w)
        self._E += 1

    def v(self):
        return self._V

    def e(self):
        return self._E

    def adj(self, v):
        """
        returns an iterable set of vertices that are adjacent to vertex v
        :param v:
        :return:
        """
        return self._adj[v]

if __name__ == '__main__':
    graph_arr = [13, 22, (0, 5), (0, 1), (2, 0), (2, 3), (3, 5), (3, 2), (4, 3), (4, 2),
                 (5, 4), (6, 9), (6, 4), (6, 8), (6, 0), (7, 6), (7, 9), (8, 6), (9, 11), (9, 10),
                 (10, 12), (11, 4), (11, 12), (12, 9)]
    print Digraph(graph_arr)._adj
