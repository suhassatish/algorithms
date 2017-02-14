"""
Given N -1 distinct integers from 1 to N-1, find the missing integer

eg - [4,1,2,6,5]
output = 3

linear time, constant space
"""


def findMissingNumber(intarr):
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


print findMissingNumber([4,1,2,6,5])
