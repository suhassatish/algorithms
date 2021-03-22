"""
Find all triplets in an integer array that sum to 0
"""


def sum3(arr):
    if arr is None or len(arr) < 3:
        return None
    arr.sort()
    s = set()
    for k in range(len(arr) - 1):
        i = k + 1
        j = len(arr) - 1
        while i < j:
            if arr[i] + arr[j] < -arr[k]:
                i += 1
            elif arr[i] + arr[j] > -arr[k]:
                j -= 1
            else:
                s.add((arr[i], arr[j], arr[k]))
                i += 1
    return s


if __name__ == '__main__':
    print(sum3([-1, -2, 0, 1, 3]))
