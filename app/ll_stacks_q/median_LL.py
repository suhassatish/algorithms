"""
Write a program that takes a pointer to an arbitrary node in a circular singly linked list
and returns the median data value of the linked list.

5->6->9->33->1   returns 6
For even number of elements, median is avg of middle 2 elements

expected linear solution with constant extra space

Corner case: circular list of all 4s, median = 4. Dont miss handling this.

"""
from llist import sllist


def median_circular_sll(arr):
    if arr is None or len(arr) == 0:
        return -1
    sll = sllist(arr)
    slow = fast = sll.first
