"""
Given 2 positive integers x and y, compute x/y by just using addition, subtraction and bit shifting
operations.

Question apparently asked to Ravi and Ashwin from IK at Facebook.
EPI Page 48, 5.6

"""


def divide(x, y):
    """
    Key insight: Find maximum k such that 2**k * y <= x;
    Cache the value of 2**k. For subsequent iterations k will always be lesser.
    quotient += 2**k

    Time complexity: If there are n-bits representing x and y, it needs n-iterations with each
    iteration having bit shifting and O(1) time, so total complexity is O(n).
    :param x:
    :param y:
    :return: Quotient from x/y
    """
    res = 0
    power = 32
    y_power = y << power

    while x >= y:
        while y_power > x:
            power -= 1
            y_power >>= 1

        x -= y_power
        res += 1 << power
    return res


if __name__ == '__main__':
    print divide(11, 2)  # 5
    print divide(49, 7)  # 7
