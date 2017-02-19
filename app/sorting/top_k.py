"""
Find k largest elements seen so far in an infinite stream

To simulate infinite stream, I use array representation, but doesnt rely on its size
Input may not be sorted and could have duplicates.

http://www.geeksforgeeks.org/k-largestor-smallest-elements-in-an-array/
"""
import heapq
from app.sorting.quick_sort_select_rank import quick_select


def top_k_streaming(arr, k):
    """
    this is the only method that works for an infinite stream
    But the code has to be modified a bit for stream

    Space = O(k)
    Time To build initial min-heap O(k)
    + to compare and insert n-k elements in worst-case = (n-k) * lg k
    Overall time = k + (n-k) lg k
    :param arr:
    :param k:
    :return:
    """
    if arr is None or len(arr) == 0 or len(arr) <= k:
        return arr

    # if it comes here, len(arr) guaranteed to be > k
    min_pq = []
    for i in xrange(k):
        heapq.heappush(min_pq, arr[i])

    for i in xrange(k, len(arr)):
        if arr[i] > min_pq[0]:  # peeks at min element of heap so far (O(1) time)
            heapq.heappop(min_pq)
            heapq.heappush(min_pq, arr[i])
    return min_pq


def top_k_linear_time(arr, k):
    """
    This is the only practical-linear time solution
    But does not work on infinite stream, needs the whole array at once
    Cannot work with a streaming solution.
    It uses quick_select to partition k times to find the pivot.
    At the kth pivot, its position in sorted order is exactly at index k, and everything to
    the right of it is in the top N - k
    :param arr:
    :param k:
    :return:
    """
    a = quick_select(arr, k)
    a
    pass


if __name__ == '__main__':
    print top_k_streaming([12, 90, -01, 789, -9, 0, 23], 3)  # [90, 789, 23]
    print top_k_linear_time([12, 90, -01, 789, -9, 0, 23], 3)
