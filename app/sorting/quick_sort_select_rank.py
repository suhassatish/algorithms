def quick_sort(arr_a):
    qsort(arr_a, 0, len(arr_a) - 1)
    return arr_a


def qsort(arr_a, lo, hi):
    """
    Best case: O(n lg n) when pivot equally partitions the array into 2 halves,
    leads to nearly balanced binary tree

    Worst case: O(n^2) when pivot is skewed towards one side, it leads to a tree which
    almost looks like a linear linked list. So O(n) * O(n). Divide-and-conquer has no benefit

    To choose a pivot which is almost at mid-way, either randomize the array in O(n) time
    But you can also choose the pivot which is arr_a[hi].

    You can also choose median of 3 random elements is the suggested approach for choosing the pivot
    This can be done in O(1) time
    :param arr_a:
    :param lo:
    :param hi:
    :return:
    """
    if hi <= lo:
        return
    j = partition(arr_a, lo, hi)
    qsort(arr_a, lo, j-1)
    qsort(arr_a, j+1, hi)


def partition(arr_a, lo, hi):
    """
    partition the subarray a[lo..hi] so that a[lo..j-1] <= a[j] <= a[j+1..hi]
    and return the index j.
    :param arr_a:
    :param lo:
    :param hi:
    :return:
    """
    i = lo
    j = hi
    v = median_3(arr_a, lo, hi, (lo+hi)/2)
    while True:
        while arr_a[i] < arr_a[v]:
            i += 1
        while arr_a[j] >= arr_a[v]:
            j -= 1

        if i >= j:
            break
        _swap(arr_a, i, j)

    _swap(arr_a, lo, j)
    return j


def _swap(arr_a, i, j):
    arr_a[i], arr_a[j] = arr_a[j], arr_a[i]
    return arr_a


def median_3(a, i, j, k):
    """
    returns index of median of 3 elements of array, among the input indices of i,j,k
    :param a:
    :return:
    """
    return sorted([(a[i], i), (a[j], j), (a[k], k)])[1][1]


def quick_select(arr_a, k):
    """
    This finds the kth minimum

    Uses quick sort's partitioning strategy
    Best case: O(n)
    Worst case: O(n^2)

    Compilers optimize for tail recursion.
    So it does take up stack space O(M) where M is depth of tree
    So to avoid this, you can use an iterative quick sort

    This finds the kth minimum
    :param arr_a:
    :param k:
    :return:
    """
    lo = 0
    hi = len(arr_a) + 1
    while hi > lo:
        j = partition(arr_a, lo, len(arr_a) - 1)
        if j < k:
            lo = j + 1
        elif j > k:
            hi = j - 1
        else:
            return arr_a[k]
    return arr_a


if __name__ == '__main__':
    print(quick_select([12, 90, -1, 789, -9, 0, 23], 1))  # not working; infinite-loop
    # print median_3([12, 90, -01, 789, -9, 0, 23], 0, 5, 2)
