"""
http://algs4.cs.princeton.edu/15uf/

The implementations below are weighted quick-union with path compression.
Construction takes O(n) time.
But after that, both union() and find() take almost amortized-constant O(1) time
"""


class UF(object):
    def __init__(self, n):
        if n < 0:
            raise ValueError("n must be a positive integer")
        self.count = n  # number of connected components
        self.parent = [i for i in range(n)]
        self.size = [0] * n  # size[i] = size of subtree rooted at i

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def find(self, p):
        """
        Returns the root of the connected component containing p
        Amortized cost per operation for this algo is bounded by a function called inverse Ackermann
        For practical purposes, this is constant O(1) time, since the fn < 5 for any practical input
        size n
        function. inv
        :param p:
        :return:
        """
        while p != self.parent[p]:
            # path-compression by halving using grand-parent links
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        return p

    def union(self, p, q):
        """
        merges the component containing p with the component containing q
        the smaller component's parent is the root of the bigger component for weighted balancing
        :param p:
        :param q:
        :return:
        """
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q:  # already part of the same component, nothing to do
            return

        # make root of smaller size point to root of larger size
        if self.size[root_p] < self.size[root_q]:
            self.parent[root_p] = root_q
            self.size[root_q] += self.size[root_p]

        else:
            self.parent[root_p] = root_q
            self.size[root_p] += self.size[root_q]

        self.count -= 1
