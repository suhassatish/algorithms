"""
Given an array, find the majority element if it exists
in linear time and constant space.

Majority is defined as frequency >n/2 where n = total number of elements in the array
"""


def majority(arr, start, end):
    n = end - start + 1
    mid = start + n/2
    if n <= 0:
        return -1

    if n == 1:
        return arr[start]

    left = majority(arr, start, mid - 1)
    right = majority(arr, mid, end)

    if left == right:
        return left

    if left != -1 and confirm_majority(arr, left, start, end):
        return left

    if right != -1 and confirm_majority(arr, right, start, end):
        return right

    return -1


def confirm_majority(arr, c, start, end):
    """
    Returns boolean whether its a majority or not
    :param arr:
    :param c:
    :param start:
    :param end:
    :return:
    """
    count = 0
    n = len(arr)
    for i in xrange(n):
        if c == arr[i]:
            count += 1
    return count > n/2
