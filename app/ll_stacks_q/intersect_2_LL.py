"""
Input: 2 singly linked lists which may or may not intersect
Output: data in the first node where intersection begins

Assume data is all positive integers or zero. You cant modify the input lists.

If they dont intersect, output = -1

Expected linear time solution with O(1) space

https://discuss.leetcode.com/topic/13419/concise-python-code-with-comments
"""
from llist import sllist


def intersect_LL(arr_a, arr_b):
    """
    this solution only works if there are no duplicate elements.
    Each pointer traverses 1st one list then the other total length O(m+n).
     If there are no intersections, then they will both reach the end together
    :param arr_a:
    :param arr_b:
    :return:
    """
    if (arr_a or arr_b) is None or len(arr_a) == 0 or len(arr_b) == 0:
        return -1
    sll_a, sll_b = sllist(arr_a), sllist(arr_b)
    pa = sll_a.first
    pb = sll_b.first
    while pa.value is not pb.value:
        pa = pa.next
        pb = pb.next
        if pa is None and pb is None:
            return -1

        if pa is None:
            pa = sll_b.first

        if pb is None:
            pb = sll_a.first

    return pa.value


if __name__ == '__main__':
    print intersect_LL([4, 5, 0, 6, 1], [7, 9, 0, 6, 1])  # 0
    print intersect_LL([4, 5, 0, 6, 1], [7, 9, 8, 16, 11])  # -1
