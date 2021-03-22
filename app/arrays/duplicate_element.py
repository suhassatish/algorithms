"""
Given an array like [2, 1, 3, 4, 5, 6, 6, 4]
return any element thats a duplicate.

Approach 1 - Hash table O(n) time, O(n) space, read-only input
Approach 2 - sort & scan; not read-only input; O(n lg n) time, O(1) space

What if range of elements is in 0 to n - 1
At each index of the array, keep the count of the element that you've seen.
From count_array, you can migrate to bit_array and flip it to 0 or 1 at an index.
You can extend this idea to keeping this bit_array into the array itself.
If you see an element, then negate it. If you have already seen an element before,
you will see a negative value. The input_array is not read_only, but you can reconstruct your
original array easily.
"""


def duplicate_element(arr):
    """
    returns an integer thats the first duplicate element encountered
    :param arr:
    :return:
    i =0 arr = [2, 1, 3, 3]
    """
    for i in range(len(arr)):
        #  if we reach a negative number, we'd already negated it before
        # we've found the duplicate element
        # have to handle 0 separately
        if arr[abs(arr[i])] < 0:
            return abs(arr[i])
        arr[abs(arr[i])] = -arr[abs(arr[i])]


if __name__ == '__main__':
    print(duplicate_element([2, 1, 3, 3]))  # 3
    print(duplicate_element([2, 1, 3, 4, 5, 6, 6, 4]))  # 6
