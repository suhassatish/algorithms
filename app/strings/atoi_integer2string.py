"""
Convert a string of digits to the corresponding integer, and vice-versa without library functions
like atoi in C++.


Corner test cases-
1) It should handle negative numbers.

2) Overflow handling
Make sure to talk about overflow and how to handle it in python.
Specifically, python2 never overflows and can handle arbitrary precision by automatically scaling
from int to long to double to arbitrary-precision floating point. Also mention how to handle
arbitrary precision floating point in a language like Java.
"""


def str2int(s):
    if s is None or len(s) == 0:
        return None

    res = 0
    sign = 1
    for c in s:
        if c == '-':
            sign = -1
            continue
        res = ord(c) - ord('0') + res * 10  # ord('0') gives ascii value of 0 = 48
    return res * sign


def int2str(num):
    if not isinstance(num, int):
        raise TypeError("{0} must be an integer".format(num))
    sign = ''
    if num < 0:
        num = abs(num)
        sign = '-'
    str_rev = []
    while num > 0:
        num, d = divmod(num, 10)
        str_rev.append(d)
    str_rev.append(sign)
    s = ''.join([str(d) for d in reversed(str_rev)])
    return s


if __name__ == '__main__':
    print str2int('-0123')  #-123
    print int2str(-123)
