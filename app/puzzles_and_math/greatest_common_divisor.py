"""
Given 2 integers, find the greatest common divisor between them.
Example - gcd(12,36) = 12

From EPI recursion chapter introduction page, the key insight is that gcd(y, x) is same as
gcd(y - x, x) if y > x. By extension, this implies gcd(y, x) = gcd(y mod x, x).
"""
from fractions import gcd


def gcd(x, y):
    """
    Time complexity analysis - Its O(log max(x, y))
    If n is the number of bits required to represent the larger of the 2 inputs, with recursion the
    space is O(n). Time complexity is also O(n). If done iteratively instead of recursively, the
    space complexity reduces to O(1)
    :param x:
    :param y:
    :return:
    """
    if y == 0:
        return x
    if x == 0:
        return y
    if y >= x:
        big = y
        small = x
    else:
        big = x
        small = y
    div, mod = divmod(big, small)
    return gcd(mod, small)


def gcd_std_lib_impl(a, b):
    """
    This is the implementation in python std lib fractions module
    Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a % b
    return a


if __name__ == '__main__':
    print gcd(12, 36)  # 12
    print gcd(156, 36)  # 12
    print gcd(13, 0)  # 13
    print gcd(-12, 36)  # 12 but returns -12, this is just a convention
    print gcd(36.3, 24.2)  # 3.5e-15 even std lib returns the same, but actual answer is 12.1
