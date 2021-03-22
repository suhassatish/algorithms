"""
["fox", "cat", "dog", "fish", "fox"] -- duplicates are possible
implement an API getShortestDist(w1, w2)

eg getShortestDist('fox', 'fish') == 1

list is big (~billions words), and we call this API ~10000 QPS
[0,4] k1, [3] k2

"""


class FindWordDist(object):
    def __init__(self, word_list):
        self.d = {}  # dict of hashed word to list of indices that it appears in. Constructed in O(n)
        for i,e in enumerate(word_list):
            if hash(e) in self.d:
                val_list = self.d[e]
            else:
                val_list = list()
            val_list.append(i)
            self.d[e] = val_list

    def get_shortest_dist(self, w1, w2):
        """
        assumes map exists of hashed key to indices in the array
        This is almost like brute-force solution.
        Takes time complexity O(k1 * k2) if k1,k2 are all indices list of w1 and w2 respectively
        """
        min_dist = float('inf')

        indices1 = []
        indices2 = []
        if w1 in self.d:
            indices1 = self.d[w1]

        if w2 in self.d:
            indices2 = self.d[w2]

        for e1 in indices1:
            for e2 in indices2:
                if abs(e1 - e2) < min_dist:
                    min_dist = abs(e1 - e2)
        return min_dist

    def get_shortest_dist2(self, w1, w2):
        """
        This method is a more optimized solution than the previous version.
        Key insight - Makes use of the property that list of indices of w1 and w2, ie k1 and k2
        are totally sorted. You want to find the min_dist between any element from k1 with any
        element from k2.

        An in-place merge-type comparison computing min_dist works in time
        O(k1 + k2) and doesn't need any auxiliary array for merge.
        You increment the pointer of the smaller element's array in each comparison.

        Other ideas I considered - If k1 is kept as a balanced binary tree,
        Tree construction needs O(k1) time + O(k1) memory. After that, Lookup k2 elements with
        min_dist in it. So total time = k1 + k2*log(k1)
        :param w1:
        :param w2:
        :return:
        """
        min_dist = float('inf')

        indices1 = []
        indices2 = []
        if w1 in self.d:
            indices1 = self.d[w1]

        if w2 in self.d:
            indices2 = self.d[w2]

        i = 0
        j = 0
        while i < len(indices1) and j < len(indices2):
            if abs(indices1[i] - indices2[j]) == 1:
                min_dist = 1
                return min_dist
            elif abs(indices1[i] - indices2[j]) < min_dist:
                min_dist = abs(indices1[i] - indices2[j])
                if indices1[i] < indices2[j]:
                    i += 1
                else:
                    j += 1

        return min_dist


if __name__ == '__main__':
    fwd = FindWordDist(["fox", "cat", "rabbit", "dog", "fish", "fox"])
    print(fwd.get_shortest_dist2('fox', 'dog'))
