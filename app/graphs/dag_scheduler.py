from topological_sort import topological_sort


class Digraph(object):

    def __init__(self, num_vertices):
        self._adj = [set() for _ in range(num_vertices)]  # _adj[0] gives the neighbors of vertex 0 -> 1
        self.v = num_vertices
        self.e = 0
        pass

    def add_edge(self, v, w):  # adds v -> w edge
        pass

    def v(self):
        return self.v

    def adj(self, v):
        return self._adj[v]


def dag_scheduler():
    NUM_NODES = 10
    g = Digraph(NUM_NODES)

    failed_jobs = []
    completed = [False]*g.v()
    for v in topological_sort(g):
        should_run = False
        for p in v.parents():  # this is the key insight, if parents failed child should not run
            if completed[p] is True:
                should_run = True
            else:
                should_run = False
                break

        if should_run:
            try:
                execute(v)
                completed[v] = True

            except:
                failed_jobs.append(v)
                # call handler to prune topologically_sorted_edges to remove dependencies of failure node
                # pruned_graph = failure_handler(failed_jobs, g)


def execute(vertex):
    pass


def failure_handler(failed_jobs_list, g):
    for v in failed_jobs_list:
        for i in g.adj(v):
            if g.has_edge(v,i):
                g.remove_edge(v, i)



