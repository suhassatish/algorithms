"""
Given a 2-player game and an array,
each player in his turn can pick a number from either end of the array.

The goal is to maximize the sum of elements you pick

eg -
[1, 4, 2, 100, 13, 6]

Hypothesis: If you take max(sum(odd_elements), sum(even_elements)), then you always win if you
start with the right side.

But its not always true, since the example [1, 4, 2, 100, 13] breaks the hypothesis.
"""