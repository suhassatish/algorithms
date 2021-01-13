"""
If get_neighbors is really cheap, you dont need explicit graph.
Else, you need to construct explicit graph so that get_neighbors() is in constant time.

Print shortest path between 2 given dictionary words (word ladder) by modifications only.
All intermediate words in word-ladder should also be dictionary words. Dict is given.

eg -
BAT -> RAP

then word ladder =
BAT -> CAT ->  CAP -> RAP

Key insight: Graph can be built offline from dict, so time for graph construction need not be
accounted for in time complexity of the algorithm.
Given dict = [BAR, BAT, CAP, CAR, CAT, HAT, RAP]

Go over n^2 pairs in dict, and see character by character if they differ by only 1 char, then
 build the Graph. Time complexity is n^2 * m

Another approach:
Maintain a hash of n * m values.
CAR -> {
    '_AR': [CAR, BAR],
    'C_R': [CAR]
    'CA_': [CAP, CAT, CAB]
}
Time complexity is n*m, memory = n * m


http://stackoverflow.com/questions/17514999/convert-string-a-to-b-using-a-dictionary-of-words
If the graph is too big to build in memory, consider using a database with one row for each edge.
"""
from itu.algs4.graphs.breadth_first_paths import BreadthFirstPaths
from itu.algs4.graphs.graph import Graph


def word_ladder(word_list, word1, word2):
    return WordLadder(word_list).word_ladder(word1, word2)


class WordLadder(object):
    """
    Assumes all words in input word_list are of same length, otherwise,
    innermost loop in constructor will degrade from O(m) to O(m^2) to compute
    levenshtein distances accounting for insertions and deletions as well.
    m = average number of letters per word
    """
    def __init__(self, word_list):
        node_count = len(word_list)
        self.word_list = word_list
        self.graph = Graph(node_count)
        self.word_to_vertex_id = {}
        for i in range(node_count - 1):
            self.word_to_vertex_id[word_list[i]] = i
            for j in range(i + 1, node_count):
                word_distance = 0
                for k in range(len(word_list[i])):
                    if word_list[i][k] == word_list[j][k]:
                        continue
                    else:
                        word_distance += 1

                    if word_distance > 1:
                        break
                if word_distance == 1:
                    # add to graph as they are adjacent nodes in the graph
                    self.graph.add_edge(i, j)

    def word_ladder(self, w1, w2):
        i1 = self.word_to_vertex_id[w1]
        i2 = self.word_to_vertex_id[w2]
        bfs = BreadthFirstPaths(self.graph, i1)
        path = []
        x = i2
        while x != i1:
            path.append(self.word_list[x])
            x = bfs.edge_to[x]
        path.append(self.word_list[x])
        return path


if __name__ == '__main__':
    d = ['BAD', 'BAR', 'BAT', 'BOT', 'CAP', 'CAR', 'CAT', 'HAD', 'HAT', 'RAP']
    a = 'BOT'
    b = 'HAD'
    print(word_ladder(d, a, b))  # BOT -> BAT -> BAD -> HAD
