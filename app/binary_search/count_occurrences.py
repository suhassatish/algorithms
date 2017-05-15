"""
Given a sorted array arr[] and a number x, write a function that counts the occurrences of x in arr[].
  Input: arr[] = {1, 1, 2, 2, 2, 2, 3,},   x = 2
  Output: 4 // 2  occurs 4 times in arr[]

Asked in Amazon AWS EMR (Palo Alto) phone screen
"""


def count_occurrences(a, x):
    """
    http://www.geeksforgeeks.org/count-number-of-occurrences-or-frequency-in-a-sorted-array/
    Approach - Use binary search to get the first occurrence of x in a[], say i
    Use binary search to get the last occurrence of x in a[], say j
    Return j - i + 1
    Time complexity = O(lg n)

    Key insight: For left-most occurrence, a[mid] == x and a[mid - 1] != x if mid - 1 is within
    array bounds
    For right-most occurrence, a[mid] == x and a[mid + 1] != x if mid + 1 is within array bounds

    :param a: The input sorted array
    :param x: the element in the array that you want to count occurrences of
    :return: -1 if x doesn't exist in a, count of number of occurrences of x in a otherwise
    """
    if a is None:
        raise ValueError
    i = _find_first_index(a, x, 0, len(a) - 1)
    if i == -1:
        return 0

    j = _find_last_index(a, x, 0, len(a) - 1)
    return j - i + 1


def _find_first_index(a, x, lo, hi):
    """
    :param a:
    :param x:
    :param lo:
    :param mid:
    :param hi:
    :param count:
    :return:
    """
    # mid = (lo + hi)/2  # in languages like java, if lo and hi are really large, (lo+hi)/2
    # might overflow. Python (cpython implementation) has auto scaling of integers to arbitrary
    # precision without overflowing
    mid = lo + (hi - lo)/2

    if hi < lo:
        return - 1

    # this is the most important condition in this problem. Notice the boundary case of mid == 0
    if a[mid] == x and (mid == 0 or a[mid - 1] != x):
        return mid

    elif x <= a[mid]:
        return _find_first_index(a, x, lo, mid - 1)

    elif x > a[mid]:
        # note: very subtle mid + 1 for binary search, to avoid infinite loop
        return _find_first_index(a, x, mid + 1, hi)


def _find_last_index(a, x, lo, hi):
    """
    :param a:
    :param x:
    :param lo:
    :param mid:
    :param hi:
    :param count:
    :return:
    """
    # mid = (lo + hi)/2  # in languages like java, if lo and hi are really large, (lo+hi)/2
    # might overflow. Python (cpython implementation) has auto scaling of integers to arbitrary
    # precision without overflowing
    mid = lo + (hi - lo)/2
    if hi < lo:
        return - 1

    # this is the most important condition in this problem.
    # Notice the boundary case of mid == len(a) - 1
    if a[mid] == x and (mid == (len(a) - 1) or a[mid + 1] != x):
        return mid

    # Notice that the order of these 2 conditions matters and is the opposite order of find first
    # method above. This biases the mid towards the end rather than the start
    elif x >= a[mid]:
        # note: very subtle mid + 1 for binary search, to avoid infinite loop
        return _find_last_index(a, x, mid + 1, hi)

    elif x < a[mid]:
        return _find_last_index(a, x, lo, mid - 1)


if __name__ == '__main__':
    print count_occurrences([0], 0)  # 1
    print count_occurrences([0], 1)  # 0
    print count_occurrences([0, 1, 2, 3, 4, 5, 6, 7, 8], 9)  # 0
    print count_occurrences([1, 1, 2, 2, 2, 2, 3], 2)  # 4
    print count_occurrences([0, 2, 2, 3, 4, 5, 6, 7, 8], 2)  # 2
