import heapq
from edge_weighted_digraph import EdgeWeightedDigraph
from index_min_pq import IndexMinPQ


class DijkstrasSP(object):
    def __init__(self, ewd, src):
        """
        :param ewd: EdgeWeightedDigraph object
        :param src: source vertex in the graph to calculate shortest paths from
        :return:
        """
        self.edge_to = [None] * ewd.v()
        # edgeTo[v] = last edge (DirectedEdge object) on shortest s->v path

        self.dist_to = [float('inf')] * ewd.v()  # distTo[v] = distance  of shortest s->v path
        self.pq = IndexMinPQ(ewd.v())  # min priority queue of vertices

        self.src = src
        self.g = ewd
        for directed_edge in self.g.edges():
            if directed_edge.wt < 0:
                # Dijkstras algorithm doesn't work for negative edge weights.
                raise ValueError("Edge {} has negative weight".format(directed_edge))

        self.dist_to[src] = 0
        # relax vertices in order of distance from src
        self.pq.insert(self.src, self.dist_to[self.src])

        while self.pq:
            v = self.pq.del_min()
            for directed_edge in self.g.adj(v):
                self.relax(directed_edge)

    def relax(self, directed_edge):
        """

        :param directed_edge: namedtuple('DirectedEdge', ['src', 'dest', 'wt'])
        :return:
        """
        v = directed_edge.src
        w = directed_edge.dest

        if self.dist_to[w] > self.dist_to[v] + directed_edge.wt:
            self.dist_to[w] = self.dist_to[v] + directed_edge.wt
            self.edge_to[w] = directed_edge
            if self.pq.contains(w):
                self.pq.decrease_key(w, self.dist_to[w])
            else:
                self.pq.insert(w, self.dist_to[w])

    def path_to(self, v):
        """
        Gives the shortest path from src s to vertex v, if it exists. Returns None otherwise (if no
        path exists from s to v).
        :param v:
        :return:
        """
        path_stk = []
        e = self.edge_to[v]
        while e:  # edge_to[src] is always None by design, hence the while loop always terminates
            path_stk.append(e)
            e = self.edge_to[e.src]

        path_stk.reverse()
        return path_stk


if __name__ == '__main__':
    graph_data = [8, 15, (4, 5, 0.35), (5, 4, 0.35), (4, 7, 0.37), (5, 7, 0.28), (7, 5, 0.28),
                  (5, 1, 0.32), (0, 4, 0.38), (0, 2, 0.26), (7, 3, 0.39), (1, 3, 0.29),
                  (2, 7, 0.34), (6, 2, 0.40), (3, 6, 0.52), (6, 0, 0.58), (6, 4, 0.93)]
    # DijkstrasSP(EdgeWeightedDigraph(graph_data), 0)
    print EdgeWeightedDigraph(graph_data).edges()
    # expected_output
    # 0 to 0 (0.00)
    # 0 to 1 (1.05)  0->4  0.38   4->5  0.35   5->1  0.32
    # 0 to 2 (0.26)  0->2  0.26
    # 0 to 3 (0.99)  0->2  0.26   2->7  0.34   7->3  0.39
    # 0 to 4 (0.38)  0->4  0.38
    # 0 to 5 (0.73)  0->4  0.38   4->5  0.35
    # 0 to 6 (1.51)  0->2  0.26   2->7  0.34   7->3  0.39   3->6  0.52
    # 0 to 7 (0.60)  0->2  0.26   2->7  0.34
