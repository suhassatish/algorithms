"""
How to find a popular element in an array, defined as if it occurs atleast 25 times.

If the array if of length 100, and if there is a popular element, it must occupy one of the indices
of 0,25,50,75
You can modify binary search will find you not just the element, but also the left-most and
right-most occurrences of the element.

Write code to find left-most element of an index and the write-most element of an index
That's a building block to quite a few problems.
------
Variant of problem: Given that the popular element occurs 50% of time, how will you find it in
constant space? Array is unsorted.

If you remove 2 elements from the array, and if they are different, throw them away.
TODO - research solution here
"""


def find_left_index(arr, begin, end, target):
    if begin == end:
        return begin
    c = (begin + end)/2
    if arr[c] < target:
        return find_left_index(arr, c + 1, end, target)
    elif arr[c] > target:
        return find_left_index(arr, begin, c - 1, target)
    elif arr[c] == target:
        if c == 0:
            return 0
        if arr[c - 1] != target:
            return c
        return find_left_index(arr, begin, c - 1, target)
