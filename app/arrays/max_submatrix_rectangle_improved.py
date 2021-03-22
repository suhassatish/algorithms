"""
http://www.geeksforgeeks.org/maximum-size-sub-matrix-with-all-1s-in-a-binary-matrix/
Given a binary matrix, find out the maximum size rectangle sub-matrix with all 1s.

"""
import sys
import random
from .largest_rectangle_under_skyline import calculate_largest_rectangle


# @include
def max_rectangle_submatrix(A):
    table = [0] * len(A[0])
    max_rect_area = 0
    # Find the maximum among all instances of the largest rectangle.
    for row in A:
        table = [x + y if y else 0 for x, y in zip(table, row)]
        max_rect_area = max(max_rect_area, calculate_largest_rectangle(table))
    return max_rect_area
# @exclude


def main():
    for _ in range(1000):
        if len(sys.argv) == 3:
            n = int(sys.argv[1])
            m = int(sys.argv[2])
        else:
            n = random.randint(1, 60)
            m = random.randint(1, 60)
        A = [[bool(random.randrange(2)) for _ in range(m)] for _ in range(n)]
        print(max_rectangle_submatrix(A))


if __name__ == '__main__':
    main()
