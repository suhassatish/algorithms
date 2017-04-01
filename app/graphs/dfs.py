"""
DEPTH-FIRST SEARCH PROPERTIES

DFS runs in O(E + V) time.

PROPOSITION: DFS marks all vertices connected to s in time proportional to
the sum of their degrees.

PROPOSITION: After DFS, can find vertices connected to s in constant time
and can find a path to s (if one exists) in time proportional to its length.

QUESTION: In a Graph G represented using the adjacency-lists representation,
depth-first search marks all vertices connected to s in time proportional to
ANSWER: The sum of the degrees of the vertices in the connected component
containing s

QUESTION: The critical data structures used in depth-first search and
breadth-first search are _____ and ____, respectively.
ANSWER: DFS->Stack BFS->Queue
EXPLANATION: With DFS, it is either an explicit stack(w/ nonrecursive version)
or the function-call stack (w/a recursive version)
"""
from graph_api import Graph


class DepthFirstPaths(object):

    def __init__(self, Grph, src):
        self.src = src
        self.edge_to = [None] * Grph.v()  # edge_to[v] = last edge on s-v path
        self.marked = [False] * Grph.v()  # marked[v] = is there an s-v path?
        self.dfs(Grph, src)

    def dfs(self, Grph, v):
        """
        Runs in O(V+E) time
        depth first search from vertex v
        :param Grph:
        :param v:
        :return:
        """
        self.marked[v] = True
        for w in Grph.adj(v):
            if not self.marked[w]:
                # import ipdb; ipdb.set_trace()
                self.edge_to[w] = v
                self.dfs(Grph, w)

    def has_path_to(self, v):
        """
        is there a path between source vertex s and vertex v?
        :param v:
        :return:
        """
        return self.marked[v]

    def path_to(self, v):
        """
        returns a path between source vertex s and vertex v, or None if it doesnt exist
        :param v:
        :return:
        """
        if not self.has_path_to(v):
            return None

        path_stk = []  # stack for path
        # walk from v to src adding the edges into the stack
        x = v
        while x != self.src:
            path_stk.append(x)  # push
            x = self.edge_to[x]
        path_stk.append(self.src)
        return path_stk

if __name__ == '__main__':
    l = [13, 13, (0, 5), (4,3), (0,1), (9, 12), (6,4), (5,4), (0,2), (11, 12), (9, 10), (0,6),
         (7,8), (9,11), (5,3)]
    g = Graph(l)
    dfp = DepthFirstPaths(g, 6)
    print dfp.edge_to  # [6, 0, 0, 5, 3, 0, None, None, None, None, None, None, None]
    print dfp.marked  # [True, True, True, True, True, True, True, False, False, False, False,
    # False, False]
    print dfp.path_to(4)  # [4, 3, 5, 0, 6]  Note: not necessarily the shortest path
