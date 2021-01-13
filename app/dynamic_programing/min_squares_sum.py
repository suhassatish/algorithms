"""
Given an integer input n, find the minimum number of squares that sum to that number.
Eg input = 61
Output = 2 (because 5**2 + 6**2 = 25 + 36 = 61)

Wrong approach -
The answer is not the highest square that is less than that number subtracted and then remaining
considered similarly, ie its not 7**2 + 3**2 + 1**2 + 1**2 + 1**2, ie 5
Notes about square root function in python 2.0 - its usually done as 9**(1/2.0)
ie, sqrt of x is syntactically computed as x ** (1/2.0). The resulting number is a float.
The float type has a method is_integer() which is True of its an integer, false otherwise.
(9**(1/2.0)).is_integer() Returns True
(8**(1/2.0)).is_integer() Returns False

Correct approach - O(n^2) using dynamic programing
http://www.geeksforgeeks.org/minimum-number-of-squares-whose-sum-equals-to-given-number-n/
So have to use a dynamic programing approach here.
"""


def min_squares_sum(n):
    if n < 0:
        raise ValueError("Number has to be a positive integer")
    dp = [float('inf')] * (n + 1)
    if n == 0:
        return 1
    if n <= 3:
        return n
    dp[0] = 1
    dp[1] = 1
    dp[2] = 2
    dp[3] = 3
    for i in range(4, n+1):
        for j in range(1, i+1):
            tmp = j * j
            if tmp > i:
                break
            if tmp == i:
                # found a perfect square, cannot get better than this
                dp[i] = 1
            else:
                dp[i] = min(dp[i], 1 + dp[i - tmp])
    return dp[n]

if __name__ == '__main__':
    print min_squares_sum(13)  # 2
    print min_squares_sum(41)  # 2
    print min_squares_sum(61)  # 2
    print min_squares_sum(100)  # 1 (10**2)
