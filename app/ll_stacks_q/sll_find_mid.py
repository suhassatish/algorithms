"""
Find the middle element in a singly linked list.

Constraint:
Do it in 1 pass over the list.
If list has even number of elements, output the 2nd of the middle 2 elements

examples -
1) input = 1->2->3->None
   output = 2
2) input = 1->11->45->12->67->89->None
   output = 12
"""
from llist import sllist  # pip install llist


def sll_find_mid(arr):
    """
    Keep a slow pointer and a fast pointer that runs at twice the speed.
    When the fast pointer reaches the end, the slow one is at the mid-point
    :param arr: Input list
    :return:
    """
    if arr is None or len(arr) == 0:
        return None

    sll = sllist(arr)
    slow = fast = sll.first

    if len(sll) in (1,2):
        return sll[-1]

    # import ipdb; ipdb.set_trace()
    while fast:
        if fast.next:
            slow = slow.next
            fast = fast.next.next
        else:
            break

    return slow.value

if __name__ == '__main__':
    print(sll_find_mid([1, 11, 45, 12, 67, 89]))  # 12
    print(sll_find_mid([1, 11, 45, 12, 67]))  # 45
    print(sll_find_mid([1, 11]))  # 11
    print(sll_find_mid([]))  # None
    print(sll_find_mid(None))  # None
