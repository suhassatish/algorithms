"""
An m by n grid a has 0s and 1s. You can move to only squares having 1s but not 0s.
 How many ways can you move from i,j = 0,0 to m-1,n-1?

eg -
1 1
1 1
total_paths = 2

1 0
1 0
total_paths = 0

1 0
0 1
total_paths = 0

1 0
1 1
total_paths = 1

1 1 1 1
1 1 1 1
1 1 1 1
total_paths = 10

Approach: In recursive solution, number of ways to get to i,j =
number of ways to get to i-1,j + number of ways to get to i,j-1.

We cache these in an auxillary 2D matrix and then add them up.

Time and space complexity = O(MN)
"""


def number_of_paths(a):
    """
    Lets do bottom-up DP, this doesn't require recursive approach
    http://www.geeksforgeeks.org/count-possible-paths-top-left-bottom-right-nxm-matrix/
    R = rows, C = columns
    :param a:
    :return:
    """
    if a[0][0] == 0:
        return 0

    R = len(a)
    C = len(a[0])
    paths = [[0 for _ in xrange(C)] for __ in xrange(R)]

    paths[0][0] = a[0][0]

    # count paths along top row, its only 1 way if there are adjacent 1s, else 0
    # if the top row is 1 0 1 1, ie after the 1st 0 is enountered, the number of paths along
    # it will be all 0s; 1 1 0 0
    for j in xrange(1, C):
        if a[0][j - 1] == 0:
            paths[0][j] = 0

            # short circuit and make all subsequent entries on this row 0s as it hit a road block
            for k in xrange(j,C):
                paths[0][k] = 0
            break # breaks out of outer for-loop

        else:
            paths[0][j] = 1

    # count paths along left-most column, its only 1 way if there are adjacent 1s, else 0
    for i in xrange(1, R):
        if a[i - 1][0] == 0:
            paths[i][0] = 0

            # short circuit and make all subsequent entries on this row 0s as it hit a road block
            for k in xrange(i,R):
                paths[0][k] = 0
            break # breaks out of outer for-loop

        else:
            paths[i][0] = 1

    for i in xrange(1, R):
        for j in xrange(1, C):
            if a[i - 1][j] == 0 and a[i][j - 1] == 0:
                paths[i][j] = 0

            elif a[i - 1][j] == 1 and a[i][j - 1] == 0:
                paths[i][j] = paths[i - 1][j]

            elif a[i - 1][j] == 0 and a[i][j - 1] == 1:
                paths[i][j] = paths[i][j - 1]

            else:
                paths[i][j] = paths[i - 1][j] + paths[i][j - 1]

    return paths[R-1][C-1]


if __name__ == '__main__':
    aa = [[1, 0], [0, 1]]
    print number_of_paths(aa)  # 0

    aa = [[1, 1], [0, 1]]
    print number_of_paths(aa)  # 1

    aa = [[1, 1], [1, 1]]
    print number_of_paths(aa)  # 2

    aa = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
    print number_of_paths(aa)  # 10 ; paths = [[1, 1, 1, 1], [1, 2, 3, 4], [1, 3, 6, 10]]

    aa = [[0, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]  # short-circuit return 0
    print number_of_paths(aa)

    aa = [[1, 0, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
    print number_of_paths(aa)  # 4 ; paths = [[1, 0, 0, 0], [1, 1, 1, 1], [1, 2, 3, 4]]
