"""
Given N -1 distinct integers from 1 to N-1, find the missing integer

eg - [4,1,2,6,5]
output = 3

linear time, constant space
"""


def find_missing_number(intarr):
    """
    we know the length of array should have been len(intarr) + 1
    :param intarr:
    :return:
    """

    # we know sum to n numbers is n * (n + 1) / 2
    n = len(intarr) + 1
    actual_sum = n * (n + 1) / 2
    observed_sum = 0
    for i in xrange(len(intarr)):
        observed_sum += intarr[i]
    return actual_sum - observed_sum

'''
Given an array of numbers sorted in increasing order, find the number of missing numbers.
arr = [2, 4, 5]  missing(arr, 0,2) = 1, missing(arr, 1,2) = 0
'''


def missing(a, start_index, end_index):
    if a is None or len(a) == 0:
        return 0

    actual_length = len(a[start_index:end_index+1])
    expected_length = a[end_index] - a[start_index] + 1
    return expected_length - actual_length


def kth_missing(a, k):
    if a is None or len(a) == 0:
        return 0

    count_missed_so_far = 0
    for i in xrange(len(a) - 1):
        nxt = i + 1
        count_missed_so_far += a[nxt] - a[i] - 1
        if count_missed_so_far < k:
            continue
        elif count_missed_so_far == k:
            # missing element is 1 less than nxt
            return a[nxt] - 1
        else:
            # iterate over the gap since,
            # we know missing element is missing in this gap
            j = a[nxt]

            # can also do away with this while loop and just add a[start] + k
            # this optimization will reduce from O(gap_width) in the inner loop to O(1)
            # if gap_width = infinity, this will never end
            while count_missed_so_far != k and j > a[i]:
                count_missed_so_far -= 1
                j = a[nxt] - 1
            return j - 1


if __name__ == '__main__':
    # print find_missing_number([4,1,2,6,5])  # 3
    # print missing([2,4,5], 0,2)  # 1
    # print missing([1,2,5,6,9], 1,2)  # 0

    # print kth_missing([1,4], 1)  # 2
    print kth_missing([1,4,6,7,9], 4)  # 3