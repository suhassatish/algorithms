from itu.algs4.graphs.digraph import Digraph
from collections import namedtuple


class EdgeWeightedDigraph(Digraph):
    def _init(self, input_stream_with_edges):
        """
        Over-rides method from itu.algs4.graphs.digraph
        :param input_stream_with_edges: This is a tuple like (src, dest, weight)
        :return:
        """
        DirectedEdge = namedtuple('DirectedEdge', ['src', 'dest', 'wt'])
        self._init_empty(input_stream_with_edges[0])
        self._E = 0
        for directed_edge in map(DirectedEdge._make, input_stream_with_edges[2:]):
            self.add_edge(directed_edge)

    def add_edge(self, directed_edge):
        """
        Over-loads parent method. Adjacency set `_adj` is a list of sets, indexed by src vertex_id.
        :param directed_edge:
        :return:
        """
        self._adj[directed_edge.src].add(directed_edge)
        self._E += 1

    def edges(self):
        """

        :return: An iterable list of DirectedEdge namedtuples in the EdgeWeightedDigraph
        """
        directed_edge_list = []
        for v in range(self._V):
            for directed_edge in self._adj[v]:
                directed_edge_list.append(directed_edge)
        return directed_edge_list
