"""
This finds a cycle in a digraph if it exists
"""
from digraph import Digraph


class DirectedCycle(object):
    """
    The constructor takes O(V+E) time.
    After that, the has_cycle takes constant O(1) time
    The directed_cycle_object.cycle takes time proportional to length of the cycle
    """
    def __init__(self, digraph_obj):
        """
        This constructor takes time proportional to O(V + E)
        :param digraph_obj:
        :return:
        """
        if not isinstance(digraph_obj, Digraph):
            raise ValueError("input must be a Digraph object")
        self._marked = [False] * digraph_obj.v()  # to keep track of visited nodes during dfs
        self._edge_to = [None] * digraph_obj.v()  # edge_to[v] = previous vertex on path to v
        self._on_stack = [False] * digraph_obj.v()  # on_stack[v] = is vertex on the stack?
        self._cycle_stk = None  # None if no cycle in digraph, else the directed cycle as a stack
        for u in xrange(digraph_obj.v()):
            if not self._marked[u] and self._cycle_stk is None:
                self._dfs(digraph_obj, u)

    def _dfs(self, digraph_obj, v):
        self._marked[v] = True
        self._on_stack[v] = True
        for w in digraph_obj.adj(v):
            # short circuit if directed cycle found
            if self._cycle_stk:
                return
            elif not self._marked[w]:
                self._edge_to[w] = v
                self._dfs(digraph_obj, w)

            # visiting a visited node again => trace back directed cycle
            elif self._on_stack[w]:
                self._cycle_stk = list()  # stack
                # now walk from v to w thru edge_to[]
                x = v
                while x != w:
                    self._cycle_stk.append(x)
                    x = self._edge_to[x]

                # in the end just add the element at the cycle head again
                self._cycle_stk.append(w)
                self._cycle_stk.append(v)

        # done iterating over v's adjacency list and didnt find any cycle, so remove from on_stack
        self._on_stack[v] = False

    def cycle(self):
        """
        Returns None if cycle doesn't exist.
        If there's a cycle, returns the nodes in the cyclical path.
        :return:
        """
        return self._cycle_stk

    def has_cycle(self):
        return True if self._cycle_stk else False

if __name__ == '__main__':
    g = Digraph([2, None, (0, 1), (1, 0)])
    print DirectedCycle(g).cycle() # should print cycle

    g = Digraph([2, None, (0, 1)])
    print DirectedCycle(g).cycle()  # should print None
