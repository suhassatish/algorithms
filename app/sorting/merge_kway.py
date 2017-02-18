"""
Merge k sorted arrays, size N each

This is a popular facebook problem. Print the sorted output.

Assume k << N. N can be unknown, eg sorted streams, sorted by timestamp etc

May have duplicates, negative numbers.

Optimal known solution is O(N k lg k) (total Nk elements,
and insertion into min-heap each time is O(log k) for k-sized heap)

Hint: realize that you dont need to access all N*k elements in otder to merge.
Merge can start with fewer elements

Extra credit: Implement priority_queue instead of library functions
"""
import heapq


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
    for k in xrange(K):
        for n in xrange(N):
            heapq.heappush(h, list_of_lists[k][n])

    # now pop from priority queue
    while h:
        out.append(heapq.heappop(h))

    return out


a = [[1, 3, 5, 7],
     [-2, 4, 5, 8],
     [0, 9, 10, 11]
    ]

# print [a[i] for i in xrange(len(merge(a)))]
print merge(a)
