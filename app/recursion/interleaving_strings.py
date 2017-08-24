"""
How many ways are there to interleave 2 strings
s1 = Yuval
s2 = Scharf

yscharf@gmail.com

At every step, you take a character from s1 or s2.
Therefore, 2^(m+n)

Given 2 strings s1 and s2 and a 3rd string s3 where
len(s3) = len(s1) + len(s2), find if s3 = is_interleaved(s1, s2)

You will usually not get 3D dynamic programing questions.
Usually, the time complexity in DP is the product of integer parameters
after dropping constant parameters.

If you pass substring as a parameter, its impossible to convert
that recursion into a DP solution.


Assuming there are interleaved heads, can I interleave the tails?
Can Tail of s1 starting from index 6 and tail of s2 starting from index 8,
can be interlevead to the tail of t.
"""

def _is_interleaved(s1, s2, k):
    pass


def is_interleaved(s1, s2, s3, i, j, k):
    pass
