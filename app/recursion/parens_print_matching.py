"""
Given N, print all valid pairs of parentheses with N pairs.
eg - brackets(1) = ()
brackets(2) = ()(), (()))
brackets(3) = ((())), ()()(), (())(), ()(()), (()())

We observe that

1) the remaining_left (after inserting some) should always be <= right_remaining
eg - this would avoid scenario like '))'

2) The termination case is when we have put down all k pairs in the prefix such that
 left_remaining = right_remaining = 0
"""


def brackets(n):
    st = set()
    _brackets(n, n, '', st)
    print st


def _brackets(left_remaining, right_remaining, prefix, valid_set):
    if left_remaining == 0 and right_remaining == 0:
        valid_set.add(prefix)
        return

    if 0 < left_remaining <= right_remaining:
        #  can still afford to insert '('
        _brackets(left_remaining - 1, right_remaining, prefix + '(', valid_set)

    if left_remaining <= right_remaining and right_remaining > 0:
        #  can still afford to insert ')'
        _brackets(left_remaining, right_remaining - 1, prefix + ')', valid_set)


if __name__ == '__main__':
    for i in range(1):
        brackets(i)
