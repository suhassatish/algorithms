"""
Given  a long integer array A[], find the max in a sliding window of size w, moving from
left to right. Sliding window moves rightward 1 position at a time.
  eg - A = [1, 3, -1, -3, 5, 3, 6, 7], w = 3

Window position                max
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7

If B[i] = max value from A[i] to A[i + w - 1], find a good optimal way to get B[i]
"""
from collections import deque


def sliding_window_max(arr, k):
    """
    Approach 1)
    By using a deque, append and pop can be accomplished from either end in O(1) time
    Finding the max of window size w is an O(w) operation. So for n-w windows, total
    time complexity is O(nw) assuming w << n

    Approach 2)
    Using a heap for window elements, we can reduce total time to approximately O(n lg w)
    But the complexity is to remove non-max elements from heap when that element slides
    out of window. This is tricky. So lets ignore this solution

    Approach 3)
    There is a trick in the deque solution to reduce the time complexity to O(n)
    1) Store only the indexes of elements in deque.

    2) If a new element comes in thats greater than the max in the deque,
    kick out all the elements in the deque before insert. This is the key step
    which ensures max element is always at w[0]. If a smaller element is inserted,
    it will be at w[pos] where pos > 0.

    3) popleft from w if it slides out of window

    4) add w[0] to max_arr if window size has been reached. This works because of step 2

    Approach 3 has been implemented below
    :return:
    """
    if arr is None or k <= 0:
        return None

    max_arr = []
    q = deque()
    for i,e in enumerate(arr):
        # if new element coming in is greater than max in q, pop all from q
        while q and arr[q[0]] < e:
            q.pop()
        q.append(i)

        # remove the element from q that has slid out of window
        if q[0] == i - k:
            q.popleft()

        # if window has reached size k, put the max into output max_arr
        if i >= k - 1:
            max_arr.append(arr[q[0]])
    return max_arr


if __name__ == '__main__':
    print(sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))
