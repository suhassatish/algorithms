

class IndexMinPQ(object):
    def __init__(self, maxN):
        self.maxN = maxN  # max number of elements on PQ
        self.n = 0  # number of elements on PQ
        self.pq = [0] * (maxN + 1)  # priority queue for the index. Binary-heap using 1-based
        # indexing

        self.qp = [-1] * (maxN + 1)  # tells if an index is contained in the PQ;
        # pq[qp[i]] = qp[pq[i]]

        self.keys = [None] * (maxN + 1)  # keys[i] = priority of i = key at index i

    def contains(self, index):
        """
        :param index: Index on priority queue
        :return: Returns True if index is contained in priority queue, false otherwise
        """
        if index < 0 or index > self.maxN:
            raise IndexError("Index out of range")
        return self.qp[index] != -1

    def del_min(self):
        """
        Removes minimum key and returns its associated index
        :return:
        """
        if self.n == 0:
            raise IndexError("Priority queue underflow")

        min_index = self.pq[1]
        self._exch(1, self.n)
        self.n -= 1
        self._sink(1)
        self.qp[min_index] = -1  # delete

        self.keys[min_index] = None  # to help with garbage collection
        self.pq[self.n + 1] = -1  # not needed
        return min_index

    def insert(self, index, key):
        """
        You cannot have more than 1 key for the same index. The keys are arranged as a min-heap.
        :param index:
        :param key:
        :return:
        """
        if index < 0 or index > self.maxN:
            raise IndexError("Index out of range")
        if self.contains(index):
            raise KeyError("Index is already in the priority queue")
        self.n += 1
        self.qp[index] = self.n
        self.pq[self.n] = index

        # once you push a key into a priority queue, there's no easy way to search for it in pq
        # hence, need to maintain a separate keys[] array to check if a key exists for an index
        self.keys[index] = key
        self._swim(self.n)

    def decrease_key(self, index, key):
        """
        Decrease the key associated with the index to the specified value
        :param index:
        :param key:
        :return:
        """
        if index < 0 or index > self.maxN:
            raise IndexError("Index out of range")

        if not self.contains[index]:
            raise KeyError("Index is not in the priority queue")

        if cmp(self.keys[index], key) <= 0:
            raise ValueError("Calling decrease_key() with given argument would not strictly"
                             " decrease the key")

        self.keys[index] = key  # now update keys_array with new key
        self._swim(self.qp[index])

    def _exch(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def _greater(self, i, j):
        return cmp(self.keys[self.pq[i]], self.keys[self.pq[j]]) > 0

    def _swim(self, k):
        while k > 1 and self._greater(k/2, k):
            self._exch(k, k/2)
            k /= 2

    def _sink(self, k):
        while 2*k <= self.n:
            j = 2 * k
            if j < self.n and self._greater(j, j + 1):
                j += 1
            if not self._greater(k, j):
                break
            self._exch(k, j)
            k = j


if __name__ == '__main__':
    s = ["it", "was", "the", "best", "of", "times", "it", "was", "the", "worst"]

    # insert a bunch of strings
    prq = IndexMinPQ(len(s))
    for i,e in enumerate(s):
        prq.insert(i, e)

    # decrease key
    prq.decrease_key(1, 'has')

    # delete and print each key
    while prq:
        indx = prq.del_min()
        print(indx, s[indx])
    # should print in alphabetical order
    # (3, 'best')
    # (0, 'it')
    # (6, 'it')
    # (4, 'of')
    # (2, 'the')
    # (8, 'the')
    # (5, 'times')
    # (1, 'was')
    # (7, 'was')
    # (9, 'worst')


