"""
edit_distance("table", "tell") -> returns 3
Number of edits to table required to make it tell, or vice versa

In recursive solution, when you try to memoize, its always in-terms of integers
since string comparison is expensive. It also gets nasty in-terms of augmenting strings.

So your recursive parameters can use integers like (i,j)
Then you can pass the strings unmodified and pass i,j instead.

Approach:
1) Define finite set of children
2) Do these children repeat? If yes, then its DP
3) If 2) is True, then its DP
"""


def edit_dist_recursive(str1, str2):
    return _edr(str1, str2)


def _edr(str1, str2, i=None, j=None):
    if i is None:
        i = len(str1) - 1  # consume upto i characters of str1

    if j is None:
        j = len(str2) - 1  # consume upto j characters of str1

    if i == 0:
        return j

    if j == 0:
        return i

    if str1[i] == str2[j]:
        return _edr(str1, str2, i-1, j-1)

    return 1 + min(_edr(str1, str2, i - 1, j),
                   _edr(str1, str2, i, j - 1),
                   _edr(str1, str2, i - 1, j - 1))


def edit_dist_iterative(str1, str2):
    """
    Time complexity = space complexity = O(MN)
    Intuition: https://www.youtube.com/watch?v=We3YDTzNXEk&index=8
    Walk along a 2 dimensional array of strings and store the edit_dist at each matrix[i][j]
        M  E  A  T
      0 1  2  3  4
    M 1 0
    E 2
    E 3
    T 4
    S 5
    Note: You have to create a matrix like above with string indexes starting from 1 as shown
    above. After this preprocessing,

    If s1[i] == s2[j]:  # its the diagonal element
        mat[i][j] = mat[i - 1][j - 1]
    else:
        mat[i][j] = min(mat[i-1][j], mat[i][j-1], mat[i-1][j-1]) + 1
    :param str1:
    :param str2:
    :return:
    """
    mat = [[0 for j in xrange(len(str2) + 1)] for i in xrange(len(str1) + 1)]
    for j in xrange(len(str2)):
        mat[0][j + 1] = j + 1

    for i in xrange(len(str1)):
        mat[i + 1][0] = i + 1

    for i in xrange(len(str1)):
        for j in xrange(len(str2)):
            if str1[i] == str2[j]:
                mat[i + 1][j + 1] = mat[i][j]
            else:
                mat[i + 1][j + 1] = 1 + min(mat[i][j + 1], mat[i + 1][j], mat[i][j])
    return mat[i + 1][j + 1]

if __name__ == '__main__':
    print edit_dist_recursive("tell", "table")  # 3
    print edit_dist_iterative("cat", "bat")  # 1
    print edit_dist_iterative("pizza", "yolo")  # 5
    print edit_dist_iterative("kitten", "sitting")  # 3
