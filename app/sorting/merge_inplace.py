"""
Given 1 sorted array of size N of positive integers (may have duplicates)
and another array of size 2N having 1st N sorted positive integers,
the 2nd half being 0s (empty) how do you merge 1st one into 2nd?

Constraint: Use O(1) memory and O(N) time.
"""


def merge_inplace(a, b):
    """
    swap the 2 halves of b so the 1st half becomes empty, then regular merge
    :param a:
    :param b:
    :return:
    """
    if a is None or len(a) == 0:
        return b
    N = len(a)
    i = k = 0
    j = N

    b = b[N:] + b[:N]
    while i < N and j < 2 * N:
        if a[i] <= b[j]:
            b[k], a[i] = a[i], b[k]
            k += 1
            i += 1
        else:
            b[k], b[j] = b[j], b[k]
            k += 1
            j += 1

    if i == N:
        # do nothing, rest of b elements are already in right place.
        pass
    elif j == 2 * N:
        # copy remaining elements of a into b
        b[k:] = a[i:]

    return b


if __name__ == '__main__':
    print(merge_inplace([2, 4, 5, 5, 123], [1, 3, 7, 7, 11, 0, 0, 0, 0, 0]))
    print(merge_inplace([1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 0, 0, 0, 0, 0]))
    print(merge_inplace([6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]))