"""
Find the longest common substring between 2 strings s1, s2

Algorithm: initialize 2-D matrix to 0s, if there's a character match,
As i index goes down and j array index goes right
(early exit optimization atend of shorter of 2 strings is not possible as you have to slide the
shorter string along every starting position of bigger string eg - CLC, ABCDEFGHIJKCL),
where you wont find 'CL' till the end)

if a[i] == b[j]:
  a) if i=0 OR j=0, increment a[i][j] to 1
  b) if i!=0 AND j!=0, a[i][j] = a[i-1][j-1] + 1
   C  L  C  L (s2)
L  0  1  0  1
C  1  0  2  0
L  0  2  0  3
C  0  0  3  0
(s1)

keep a rolling max variable, and a longest array result_set
init:
i=0, j=0, max = 0, result_set = {}
i=0, j=1, max = 1, result_set = {L}
i=0, j=3, max = 1, result_set = {L}
i=1, j=0, max = 1, result_set = {L, C}
i=1, j=2, max = 2, result_set = {LC}
i=2, j=1, max = 2, result_set = {LC, CL}
i=2, j=3, max = 3, result_set = {LCL}
i=3, j=2, max = 3, result_set = {LCL, CLC}

time complexity: O (n^2)
space : O(MN) where M = length(s1), N = length(s2)

Explanation:
https://www.youtube.com/watch?v=tABtJbLOQho
"""


def longest_common_substring(s1, s2):
    """
    :param s1: input string s1
    @type s1: str

    :param s2: input string s2
    @type s2: str

    :return: set of longest common substrings.
    empty set, if 1 of the inputs is empty
    None, if 1 of the inputs is None
    """
    if s1 is None or s2 is None:
        return None
    elif len(s1) == 0 or len(s2) == 0:
        return set("")
    else:
        matrix = [[0 for j in xrange(len(s2))] for i in xrange(len(s1))]
        rolling_max = 0
        result = set()
        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    if i == 0 or j == 0:
                        matrix[i][j] = 1
                    else:
                        matrix[i][j] = matrix[i-1][j-1] + 1

                    # if you find a longer substring than the max seen so far, reinitialize the set
                    if matrix[i][j] > rolling_max:
                        rolling_max = matrix[i][j]
                        result = set()
                        result.add(s1[i+1-rolling_max:i+1])

                    elif matrix[i][j] == rolling_max:
                        result.add(s1[i+1-rolling_max:i+1])
                else:
                    matrix[i][j] = 0

    # although returning the whole set is a desirable behaviour, for a Database function
    # implementation, its better to return a deterministic first match as a string instead of a set.
    # Also, the set is unlikely to have more than 1 element of the same length
    return sorted(result)[0]
