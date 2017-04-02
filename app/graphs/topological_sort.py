"""
Topological sort doesn't work if there is a cycle in the graph.

C1 -> C2
|      |
V      V
C3    C6 -> C5
  ^         ^
   \        |
    C4 -----

Output: topologically sorted order = [C1, C2, C4, C3, C6, C5]

Implementation: DFS with global stack.
Once you're done processing on a node, you push it onto a stack.
stk = [C5, C6, C2, C3, C1, C4]

Order is stk.reverse()

Another problem: Decipher alien language alphabet from a bunch of encrypted words.
eg - this is the dictionary order of words in alphabetic order:
[dbc, dba, dcb, dca, bdc, bda]

http://www.geeksforgeeks.org/topological-sorting/
DFS order is different from topological sort order in many cases. Topological sort keeps a stack.

DFS algo - Print a node, and then recursively call DFS on adj_nodes.

Topo-sort algo - We dont print vertex immediately,  we first recursively call topo_sort on adj_nodes
Then push node to a stack. Finally print contents of stack.


http://www.geeksforgeeks.org/given-sorted-dictionary-find-precedence-characters/
"""

from digraph import Digraph
from directed_cycle import DirectedCycle


def find_order(word_sorted_list):
    """
    Given a list of words in an alien language in dictionary sorted order, return the alphabetical
    order of the letters in the alien language.

    The algorithm is as follows:
    1) Find the number of letters in the alphabet, by going 1 pass over the input array.
        This takes time O(wl). if there are w words and l letters on an avg per word.
        Lets call the result, alpha

    2) Create a digraph with num_vertices = alpha

    3) For every pair of consecutive words (word1, word2) in the input list (there are w - 1 pairs
    in a w-word list),  compare letters of word1 & word2 until you find the 1st mismatching
        character. Add an edge in the digraph from letter in word1 to letter in word2

    4) Topologically sort the digraph. This takes time O(V + E) = O(alpha + alpha - 1)

    Total time = O(wL) + O(1) + O[(w-1)(L)] + O(alpha)
                = O(wL) where L = avg number of letters per word
    :param word_sorted_list:
    :return:
    """
    alphabet = set()
    for word in word_sorted_list:
        for letter in word:
            alphabet.add(letter)
    num_vertices = len(alphabet)

    dg = Digraph(num_vertices)

    # graph takes vertex values as integers,
    # so using 2 maps for letter -> vertex_id and inverse mapping
    letter_to_vertex_id_dict = {}
    vertex_id_to_letter = []

    for i in xrange(len(word_sorted_list) - 1):
        word1 = word_sorted_list[i]
        word2 = word_sorted_list[i + 1]
        if len(word1) < len(word2):
            smaller_word = word_sorted_list[i]
        else:
            smaller_word = word_sorted_list[i + 1]
        for word_index in xrange(len(smaller_word)):
            if word1[word_index] == word2[word_index]:
                continue
            else:
                letter1 = word1[word_index].lower()
                letter2 = word2[word_index].lower()
                vertex1 = _get_vertex_for_letter(letter1, letter_to_vertex_id_dict,
                                                 vertex_id_to_letter)

                vertex2 = _get_vertex_for_letter(letter2, letter_to_vertex_id_dict,
                                                 vertex_id_to_letter)
                dg.add_edge(vertex1, vertex2)

                # no need to consider other characters in this word pair,
                # break out of inner for-loop
                break

    # now just do a topological sort of the letters
    ordered_vertex_ids = topological_sort(dg)
    lst = [vertex_id_to_letter[vertex] for vertex in ordered_vertex_ids]
    return ''.join([i for i in lst])


def _get_vertex_for_letter(letter, letter_to_vertex_id_dict, vertex_id_to_letter):
    if letter in letter_to_vertex_id_dict:
        vertex = letter_to_vertex_id_dict.get(letter)
    else:
        # generate a vertex_id
        vertex_id_to_letter.append(letter)
        vertex = len(vertex_id_to_letter) - 1
        letter_to_vertex_id_dict[letter] = vertex
    return vertex


def topological_sort(digraph_obj):
    """
    The constructor takes time proportional to V + E
    (in the worst case),
    where V is the number of vertices and E is the number of edges.
    :param digraph_obj:
    :return:
    """
    if not isinstance(digraph_obj, Digraph):
        raise ValueError("Input to method must be a digraph object")
    visited = [False] * digraph_obj.v()
    stk = []
    if DirectedCycle(digraph_obj).has_cycle():
        return None

    for u in xrange(digraph_obj.v()):
        if not visited[u]:
            _ts(digraph_obj, u, visited, stk)

    stk.reverse()  # equivalent to popping from stack
    return stk  # list of all elements in topologically sorted order


def _ts(digraph_obj, v, visited, stack):
    """
    :param digraph_obj: the directed graph
    :param v: current node in graph
    :param visited: boolean list
    :param stack: stack that keeps the topologically sorted order which is finally returned
    :return:
    """
    # Mark the current node as visited.
    visited[v] = True

    # Recur for all the vertices adjacent to this vertex
    for u in digraph_obj.adj(v):
        if not visited[u]:
            _ts(digraph_obj, u, visited, stack)

    # Once you're done processing on a node & its adjacent nodes, you push it onto the stack.
    stack.append(v)


if __name__ == '__main__':
    g = Digraph([6, None, (5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (1, 3)])
    print topological_sort(g)  # [5, 4, 2, 1, 3, 0]

    # tests a cyclic digraph, topological_sort should detect cycle and return None
    g = Digraph([2, None, (0, 1), (1, 0)])
    print topological_sort(g)  # None

    print find_order(['baa', 'abcd', 'abca', 'cab', 'cad'])  # bdac
    print find_order(['caa', 'aaa', 'aab'])  # cab
    print find_order(['aa', 'bb', 'cc', 'dd', 'ee'])  # abcde
