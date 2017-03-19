#!/bin/python

"""
https://www.hackerrank.com/contests/june-world-codesprint/challenges/equal-stacks
You have three stacks of cylinders where each cylinder has the same diameter, but they may vary in height.
You can change the height of a stack by removing and discarding its topmost cylinder any number of times.

Find the maximum possible height of the stacks such that all of the stacks are exactly the same height.
This means you must remove zero or more cylinders from the top of zero or more of the three stacks until
they're all the same height, then print the height. The removals must be performed in in such a way as
to maximize the height.

Note: An empty stack is still a stack.

Input Format

The first line contains three space-separated integers, , , and , describing the respective number of
cylinders in stacks , , and . The subsequent lines describe the respective heights of each cylinder in a
stack from top to bottom:

The second line contains  space-separated integers describing the cylinder heights in stack .
The third line contains  space-separated integers describing the cylinder heights in stack .
The fourth line contains  space-separated integers describing the cylinder heights in stack .
Constraints

Output Format

Print a single integer denoting the maximum height at which all stacks will be of equal height.

Sample Input

5 3 4
3 2 1 1 1
4 3 2
1 1 4 1
Sample Output

5
"""


def find_tallest_equal_stack(m1, m2, m3, stack1, stack2, stack3):
    inputs = [m1, m2, m3] + stack1 + stack2 + stack3
    if len(filter(zero_or_negative, inputs)) > 0 \
            or len(stack1) != m1 or len(stack2) != m2 or len(stack3) != m3:
        return 0
    else:
        set1 = _get_cumulative_height_set(stack1)
        set2 = _get_cumulative_height_set(stack2)
        set3 = _get_cumulative_height_set(stack3)
        equal_heights = set1.intersection(set2).intersection(set3)
        if len(equal_heights) > 0:
            return max(equal_heights)
        else:
            return 0


def _get_cumulative_height_set(stack_array):
    cumulative_height_set = set()
    cumulative_height = 0
    for element in reversed(stack_array):
        cumulative_height += element
        cumulative_height_set.add(cumulative_height)
    return cumulative_height_set


def zero_or_negative(element):
    return element <= 0


if __name__ == "__main__":
    n1,n2,n3 = raw_input().strip().split(' ')
    n1,n2,n3 = [int(n1),int(n2),int(n3)]
    try:
        a1 = map(int, raw_input().strip().split(' '))
    #an empty stack is still a stack
    except ValueError:
        a1 = []
    try:
        a2 = map(int, raw_input().strip().split(' '))
    except ValueError:
        a2 = []
    try:
        a3 = map(int, raw_input().strip().split(' '))
    except ValueError:
        a3 = []
    print find_tallest_equal_stack(n1, n2, n3, a1, a2, a3)