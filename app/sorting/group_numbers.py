"""
Group a list of positive integers into even and off, in-place in O(n) time
All even numbers should appear first
"""


def group_numbers(arr):
    if arr is None or len(arr) == 0:
        return arr
    i = 0
    j = len(arr) - 1
    while True:
        while arr[i] % 2 == 0:  # while even keep going; stops at odd
            i += 1
            if i == len(arr):
                break

        while arr[j] % 2 != 0:  # while odd keep going; stops at even
            j -= 1
            if j == 0:
                break

        if i >= j:
            break
        arr[i], arr[j] = arr[j], arr[i]

    return arr


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6, 10, 8]
    print group_numbers(a)
    print group_numbers([1, 1])
