"""
Given an array of nuts and an array of bolts, match the nuts to the bolts of the same size.
Assume 1:1 mapping between nuts to bolts.
Nuts cannot be compared against each other, ie no sorting them.
Bolts cannot be compared against each other, ie no sorting them
Nuts can only be compared to bolts and vice versa

http://www.geeksforgeeks.org/nuts-bolts-problem-lock-key-problem/
"""


def match(nuts_arr, bolts_arr):
    """
    Given: nuts_arr and bolts_arr of equal length
    :param nuts_arr:
    :param bolts_arr:
    :return: Returns a set of matched pairs of nuts and bolts
    """
    _match(nuts_arr, bolts_arr, 0, len(nuts_arr) - 1)
    # print nuts_arr, bolts_arr
    # bolts_arr at this point is almost sorted but needs 1 rotation, eg [4, 1, 2, 3]
    return set(zip(nuts_arr, bolts_arr[1:] + bolts_arr[:1]))


def _match(nuts_arr, bolts_arr, lo, hi):
    """
    :param nuts_arr:
    :param bolts_arr:
    :param lo: start index, int
    :param hi: end index, int
    :return:
    """
    # print nuts_arr, bolts_arr, lo, hi
    if hi <= lo:
        # for 0-sized list, lo = 0 , hi = len(list) = 0
        return

    # instead of bolts_arr[hi], you can choose seed_pivot as median of 3 random
    # elements drawn from bolts_arr
    # choose last element of bolts array for nuts partition
    j = _partition(nuts_arr, lo, hi, bolts_arr[hi])
    # print j

    # now using the partition of nuts, choose that for bolts partition
    _partition(bolts_arr, lo, hi, j)

    # recurse on subarrays but excluding the chosen partition j
    _match(nuts_arr, bolts_arr, lo, j-1)
    _match(nuts_arr, bolts_arr, j+1, hi)


def _partition(arr, lo, hi, pivot):
    """
    Regular partition function of quick sort, but with an extra argument pivot
    :param arr:
    :param lo:
    :param hi:
    :param pivot:
    :return:
    """
    i = lo
    j = hi
    while True:
        while arr[i] < pivot:
            i += 1
            if i == hi:
                break

        while arr[j] > pivot:
            j -= 1
            if j == lo:
                break

        if i >= j:
            break
        _swap(arr, i, j)

    _swap(arr, lo, j)
    return j


def _swap(a, index1, index2):
    """
    Swap 2 elements in a list
    :param a: a list
    :param index1: index1 to be swapped, int
    :param index2: index2 to be swapped, int
    :return: input list a with elements at index1, index2 swapped
    """
    a[index1], a[index2] = a[index2], a[index1]
    return a
