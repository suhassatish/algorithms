"""
Vertex (V) and edge (E)
Directed vs undirected graphs

Cyclic vs acyclic graphs.

eg - loop in a linked list = cyclic directed graph. Linked lists and trees are subsets of graphs.

Degree of a vertex. In-degree = number of incoming edges ,
 out-degree (default) = number of outgoing edges.

Degree of a graph - Maximum degree of any node.

Connected component of a vertex: All vertices that are reachable from current vertex.
1-> 2-> 3-> 4->5->6
^-----------------|


Click in a graph is every vertex is connected to every other vertex (fully connected)

Sink: Vertex that has in-degree, but not out-degree.

Implementation: Usually as adjacency_matrix and adjacency_list

Adjacency matrix:
   0  1  2  3  4
0        1     1
1  1  1
2           1  1
3  1  1  1  1  1
4

Adjacency list:
{
    0: [2, 4],
    1: [0, 1],
    2: [3, 4],
    3: [0, 1, 2, 3, 4],
    4: []
}

Pros & Cons:
adj_matrix can answer in constant time. TODO: revisit video lecture
adj_list takes time = degree of graph


adj_matrix = not good for sparse graphs
adj_list = not good for dense graphs
adj_set can be good for anything.

Weighted vs unweighted graphs. Edges carry weights.

Traversal: breadth-first search (bfs) and depth-first search (dfs)
Anything you do recursively can be done iteratively using a stack.
But the vice-versa is not true.

Litmus tests for graph problems:
Safest way is by doing bfs, will not have any stack overflows.
Dfs is the shortest way to do it.

There are 2 kinds of graph problems:
1) Its obvious that its a graph problem. Explicit graph problems
2) Implicit graph problems

Clone entire connected component of a given vertex. Return the clone. Dont forget to clone the
edges as well. Have a hash map of original to clone. This can serve as the visited set. Can do it
using both bfs or dfs.

"""


class Graph(object):
    def __init__(self, a):
        if isinstance(a, int):
            self._init_empty(a)
        elif isinstance(a, Graph):
            self._init_from_graph(a)
        elif isinstance(a, list) and len(a) == 1:
            self._init_empty(a[0])
        elif isinstance(a, list):
            self._init(a)

    def _init_empty(self, num_vertices):
        if num_vertices < 0:
            raise Exception("Number of vertices must be non-negative")
        self._adj = [None] * num_vertices  # this is an adjacency_list indexed by vertex
        self._V = num_vertices
        self._E = 0

        # each indexed element is a set of nodes that are connected to this vertex
        for v in range(num_vertices):
            self._adj[v] = set()

    def _init(self, input_stream_with_edges):
        """
        The format of input_stream_with_edges is a list.
        The number of vertices is lst[0], lst[1] = number_of_edges , lst[2:] = tuple of edges
        :param input_stream_with_edges:
        :return:
        """
        self._init_empty(input_stream_with_edges[0])
        self._E = 0
        for v,w in input_stream_with_edges[2:]:
            self.add_edge(v, w)

    def _init_from_graph(self, graph_obj):
        """
        This deep copies the input graph_obj to create a cloned graph.
        Sample inputs to test with -
        1) Single node graph
        2) A binary tree graph
        3) A linked list graph
        4) A cyclic graph with a loop
        :return:
        """
        self._init_empty(graph_obj.v())
        self._E = graph_obj.e()
        for v in range(graph_obj.v()):
            for w in graph_obj.adj(v):
                self._adj[v].add(w)

    def add_edge(self, v, w):
        """
        Adds the undirected edge v-w to self graph
        :param v:
        :param w:
        :return:
        """
        self._adj[v].add(w)
        self._adj[w].add(v)
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
