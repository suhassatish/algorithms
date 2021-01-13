"""
Merge k sorted arrays, size N each

This is a popular facebook problem. Print the sorted output.

Assume k << N. N can be unknown, eg sorted streams, sorted by timestamp etc

May have duplicates, negative numbers.

Optimal known solution is O(N k lg k) (total Nk elements,
and insertion into min-heap each time is O(log k) for k-sized heap)

Hint: realize that you dont need to access all N*k elements in order to merge.
Merge can start with fewer elements

Extra credit: Implement priority_queue instead of library functions

Related question - external sorting.

Another variant of the question -
https://stackoverflow.com/questions/7153659/find-an-integer-not-among-four-billion-given-ones?rq=1

"""
import heapq
from llist import sllist


def merge(list_of_lists):
    if list_of_lists is None or len(list_of_lists) == 0:
        return list_of_lists

    K = len(list_of_lists)
    N = len(list_of_lists[0]) # input specification = all sublists are of equal length
    h = []
    out = []
    # push all elements into the priority queue (needs memory O(NK))
    # If its infinite stream, this wont work. Then you will have to maintain
    # priority queue of size k only
    for k in range(K):
        for n in range(N):
            heapq.heappush(h, list_of_lists[k][n])

    # now pop from priority queue
    while h:
        out.append(heapq.heappop(h))

    return out


def merge_infinite(list_of_lists):
    """
    This is different from the above method in that it uses a linked-list under the hood
    It also uses fixed-windows of size Nk elements and merges them before sliding to the next
    non-overlapping window. The size of priority queue is no greater than k at any given point

    A last pass is required to merge all the windows
    We show the computation for 1 window only
    :param list_of_lists:
    :return:
    """
    K = len(list_of_lists)
    N = len(list_of_lists[0])
    if list_of_lists is None or len(list_of_lists) == 0:
        return list_of_lists
    h = []
    out = []
    list_of_linked_lists = []
    for lst in list_of_lists:
        # converts each of the k-lists into a singly-linked-list
        # total time = O(Nk)
        list_of_linked_lists.append(sllist(lst))

    while len(out) != N * K:
        # push upto k elements at a time into pq. Takes O(lg k)
        for k in range(K):
            if list_of_linked_lists[k].first is not None:
                # remove the head of corresponding linked list and advance its pointer
                # this is an O(1) operation
                heapq.heappush(h, list_of_linked_lists[k].popleft())

        item = heapq.heappop(h)  # this is an O(1) operation in min-heap
        out.append(item)

    return out


class Node(object):
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next


if __name__ == '__main__':
    a = [[1, 3, 5, 7],
         [-2, 4, 5, 8],
         [0, 9, 10, 11]
        ]

    # print [a[i] for i in range(len(merge(a)))]
    # print merge(a)
    print merge_infinite(a)
