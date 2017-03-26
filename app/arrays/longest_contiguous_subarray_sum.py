"""
Find contiguous subarray of maximum sum in an array of positive and negative integers

eg -                               [2, 4, -5, 6, -10, 21,  4]
cumulative_sum =                   [2, 6, 1, 7,  - 3, 18, 22] (A)
min_cum_sum; starting with 0 =    [0, 0, 0, 0,  - 3, -3, -3] (B)

do A - B at each step              [2, 6, 1, 7,    0, 21, 25]
also keep an array of indices for A,B.
Hence, it works in a greedy way with O(n). Some people incorrectly call it  dynamic programing
"""