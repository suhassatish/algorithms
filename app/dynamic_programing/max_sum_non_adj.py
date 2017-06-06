"""
Given an array of positive integers, find the max sum of sequence of non-adjacent elements
[4, 2, 100, 900, 1005, 1000]

this should return [4, 900, 1000] since 4 + 900 + 1000 = 1904 = max sum
"""


def max_sum_non_adj(arr):
    if len(arr) == 1:
        return arr[0]

    p = [arr[0], max(arr[0], arr[1])]
    for i in range(2, len(arr)):
        p.append(max(p[i-1], p[i-2] + arr[i]))
    return p[-1]

if __name__ == '__main__':
    print max_sum_non_adj([4, 2, 100, 900, 1005, 1000])  # 1904
