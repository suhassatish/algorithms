"""
There is no solution for grid 2x2 or 3x3

| | |Q| |
|Q| | | |
| | | |Q|
| |Q| | |
This is the solution for 4x4
Its a backtracking problem, because we place a queen and then check
if that queen threatens existing queens on the board.

Place n queens on a square n x n  chess board so that they dont threaten each other.
Prints all solutions to the N queens problem

Approach 1:
In this problem, whenever a location (x, y) is occupied,
any other locations (p, q ) where p + q == x + y (1 diagonal) or p - q == x - y (other diagonal)
would be invalid.
We can use this information to keep track of the indicators (xy_dif and xy_sum )
of the invalid positions and then call DFS recursively with valid positions only
https://discuss.leetcode.com/topic/20217/fast-short-and-easy-to-understand-python-solution-11-lines-76ms/6
"""


def queens(n):
    """
    You try to convert the 2D problem into 1 dimension by only storing a 1D list,
    where each element in the list is the index of the placed queen on that column (file)
    eg - for queens(4), 1 solution looks like [2,0,3,1]
    :param n:
    :return:
    """
    l = [None] * n  # initializes a list of size-n with all None elements
    _queens_recursion(l, 0)


def _queens_recursion(arr, i):
    """
    Better to have length of arr as a constant and keep changing integer i in recursive fn argument
    This is a standard technique to memoize any recursive call to convert it into a DP solution
    :param arr:
    :param i:
    :return:
    """
    if i == len(arr):
        #  you can also add boiler-plate code to print board here
        print_chess_board(arr),
        return

    for j in range(len(arr)):
        arr[i] = j

        # standard pattern for back tracking. If conditional check within for-loop in recursive fn
        if is_valid(arr, i):
            _queens_recursion(arr, i + 1)


def print_chess_board(arr):
    for e in arr:
        print("+-"),
    print('+')

    for k in range(len(arr)):
        for e in arr:
            print("|" + ('Q' if e == k else ' ')),
        print("|")

        for e in arr:
            print("+-"),
        print("+")
    print


def is_valid(arr, i):
    for k in range(i):
        # if anything previously has been placed on the same row (rank),
        # current placement is invalid
        if arr[k] == arr[i]:
            return False

        # 1-dim reduction of problem ensures that you dont place a queen on the same file (column)
        # so no need to check for this

        # next check for the 2 diagonals
        if arr[k] - arr[i] == k - i:
            return False

        if arr[k] - arr[i] == i - k:
            return False

    return True


if __name__ == '__main__':
    print(queens(4))
    """
    +- +- +- +- +
    |  |  |Q |  |
    +- +- +- +- +
    |Q |  |  |  |
    +- +- +- +- +
    |  |  |  |Q |
    +- +- +- +- +
    |  |Q |  |  |
    +- +- +- +- +

    +- +- +- +- +
    |  |Q |  |  |
    +- +- +- +- +
    |  |  |  |Q |
    +- +- +- +- +
    |Q |  |  |  |
    +- +- +- +- +
    |  |  |Q |  |
    +- +- +- +- +
    """
