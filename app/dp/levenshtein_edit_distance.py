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


if __name__ == '__main__':
    print edit_dist_recursive("tell", "table")  # 3
