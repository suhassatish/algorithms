"""
Find contiguous subarray of maximum sum in an array of positive and negative integers

eg -                               [2, 4, -5, 6, -10, 21,  4]
cumulative_sum =                   [2, 6, 1, 7,  - 3, 18, 22] (A)
min_cum_sum; starting with 0 =    [0, 0, 0, 0,  - 3, -3, -3] (B)

do A - B at each step              [2, 6, 1, 7,    0, 21, 25]
also keep an array of indices for A,B.
Hence, it works in a greedy way with O(n). Some people incorrectly call it  dynamic programing
"""


#          (1, 2, -4, 1, 3, -2, 3, -1
# cum_sum   1, 3, 0,  1, 4, 2,  5, 4
# msf       1, 3, 3,  3, 4, 4,  5, 5
def max_sum(a):
    cum_sum = 0
    max_so_far = -float('inf')
    for e in a:
        if cum_sum + e < 0:
            cum_sum = 0
        else:
            cum_sum += e
        if cum_sum > max_so_far:
            max_so_far = cum_sum
    return max_so_far
