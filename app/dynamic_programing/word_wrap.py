# -*- coding: utf-8 -*-
"""
http://www.geeksforgeeks.org/dynamic-programming-set-18-word-wrap/
Slightly different variation - https://leetcode.com/problems/text-justification/description/

Given a sequence of words, and a limit on the number of characters that can be put in one line (line width). Put line
breaks in the given sequence such that the lines are printed neatly. Assume that the length of each word is smaller than
 the line width.

The word processors like MS Word do task of placing line breaks. The idea is to have balanced lines. In other words, not
 have few lines with lots of extra spaces and some lines with small amount of extra spaces.

The extra spaces includes spaces put at the end of every line except the last one.
The problem is to minimize the following total cost.
 Cost of a line = (Number of extra spaces in the line)^3
 Total Cost = Sum of costs for all lines

For example, consider the following string and line width M = 15
 "Geeks for Geeks presents word wrap problem"

Following is the optimized arrangement of words in 3 lines
Geeks for Geeks
presents word
wrap problem

The total extra spaces in line 1, line 2 and line 3 are 0, 2 and 3 respectively.
So optimal value of total cost is 0 + 2*2 + 3*3 = 13
Please note that the total cost function is not sum of extra spaces, but sum of cubes (or square is also used) of extra
spaces. The idea behind this cost function is to balance the spaces among lines. For example, consider the following two
 arrangement of same set of words:

1) There are 3 lines. One line has 3 extra spaces and all other lines have 0 extra spaces.
Total extra spaces = 3 + 0 + 0 = 3. Total cost = 3*3*3 + 0*0*0 + 0*0*0 = 27.

2) There are 3 lines. Each of the 3 lines has one extra space. Total extra spaces = 1 + 1 + 1 = 3.
Total cost = 1*1*1 + 1*1*1 + 1*1*1 = 3.

Total extra spaces are 3 in both scenarios, but second arrangement should be preferred because extra spaces are balanced
 in all three lines. The cost function with cubic sum serves the purpose because the value of total cost in second
 scenario is less.

This problem is also called justify_text.py in EPI.

"""


def justify_text(words, L):
    curr_line_length, result, curr_line = 0, [], []
    for word in words:
        if curr_line_length + len(word) + len(curr_line) > L:
            # Distribute equally between words in curr_line.
            for i in range(L - curr_line_length):
                curr_line[i % (len(curr_line) - 1 or 1)] += ' '
            result.append(''.join(curr_line))
            curr_line, curr_line_length = [], 0
        curr_line.append(word)
        curr_line_length += len(word)
    # Use ljust(L) to pad the last line with the appropriate number of blanks.
    return result + [' '.join(curr_line).ljust(L)]
# @exclude


def test_case(words, L, golden):
    result = justify_text(words, L)
    for s in result:
        print("'%s'" % s)
    print()
    assert result == golden


def main():
    words = ['Text', 'justification', 'is', 'trickier', 'than', 'it', 'seems!']
    golden = [
        'Text          ', 'justification ', 'is    trickier', 'than it seems!'
    ]
    L = 14
    print('L =', L)
    test_case(words, L, golden)
    words = ['Listen', 'to', 'many,', 'speak', 'to', 'a', 'few.']
    golden = ['Listen', 'to    ', 'many, ', 'speak ', 'to   a', 'few.  ']
    L = 6
    print('L =', L)
    test_case(words, L, golden)
    words = [
        'The', 'quick', 'brown', 'fox', 'jumped', 'over', 'the', 'lazy', 'dogs.'
    ]
    golden = [
        'The   quick', 'brown   fox', 'jumped over', 'the    lazy',
        'dogs.      '
    ]
    L = 11
    print('L =', L)
    test_case(words, L, golden)
    golden = ['The  quick brown', 'fox  jumped over', 'the lazy dogs.  ']
    L = 16
    print('L =', L)
    test_case(words, L, golden)
    golden = ['The  quick  brown', 'fox  jumped  over', 'the lazy dogs.   ']
    L = 17
    print('L =', L)
    test_case(words, L, golden)
    words = ['Hello', 'World']
    golden = ['Hello World   ']
    L = 14
    test_case(words, L, golden)


if __name__ == '__main__':
    main()
