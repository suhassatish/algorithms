"""
Given rope of length n, cut into m parts such that
product of lengths n[0]*n[1]*n[m-1] is maximized.

We have to cut once at least.
Length of whole rope as well as chunks are +ve integers.
Assume length is atleast 2 units

eg -
For n = 1 , max_prod(1) = 0 (since we cant cut at all)
max_prod(2) = 1 (1*1)
max_prod(3) = 2 (1*2)
For n = 4, (1,3), (2,2), (1,1,2) are possible. But we choose 2,2 since 2* 2 = 4
max_prod(5) = 3*2 = 6
max_prod(6) = 3 * 3 = 9 > 2*4
max_prod(7) = 4 * 3 = 12 > 5 * 2
For n = 10, output = 3,3,4 since 3*3*4 = 36 = maximal product

For n = 58, output = 1549681956
"""


def max_prod(m):
    return _max_prod(m, m)


def _max_prod(rope_size, initial_rope_size):
    if rope_size == 1:
        return 1

    mx = 0 if rope_size == initial_rope_size else rope_size
    for i in range(1, rope_size):
        mx = max(mx, i * _max_prod(rope_size - i, initial_rope_size))

    return mx


def max_prod_dp(rope_length):
    """
    For j = 2,
        mx_arr[] = _ 1
        index      0 1 2

        mx_arr[2] = max(1 * mx_arr[1])

    For j = 3,
        mx_arr[] = _ 1 1
        index      0 1 2 3

        mx_arr[3] = max(1 * mx_arr[2], 2 * mx_arr[1])

    For j = 4,
        mx_arr[] = _ 1 1 2
        index      0 1 2 3 4

        mx_arr[4] = max(1 * mx_arr[3], 2 * mx_arr[2], 3 * mx_arr[1])
    :param rope_length:
    :return:
    """
    if rope_length <= 2:
        return 1

    mx_arr = [0 for _ in range(rope_length + 1)]
    mx_arr[1] = 1
    for j in range(2, rope_length + 1):
        mx_val = 0 if j == rope_length else j
        for i in range(1, j):
            mx_val = max(mx_val, i * mx_arr[j - i])
        mx_arr[j] = mx_val
    return mx_arr[rope_length]

if __name__ == '__main__':
    print max_prod_dp(2)  # 1
    print max_prod_dp(3)  # 2
    print max_prod_dp(4)  # 4
    print max_prod_dp(5)  # 6
    print max_prod_dp(6)  # 9
    print max_prod_dp(7)  # 12
