# -*- coding: utf-8 -*-
"""
Problem:
Given a histogram, find the area of the largest rectangle enclosed by it

Algorithm:
1) initialize 2 stacks - 1 for max_index and another for max_value

2)
Start from first bar, and do following for every bar ‘hist[i]’ where ‘i’ varies from 0 to n-1
  a) If stack is empty or hist[i] is higher than the bar at top of stack, then push index, value onto both stacks.
  b) If this bar is smaller than the top of stack, then
      i) keep removing the top of max_value stack while top of the stack is greater
     ii) Let the removed bar be hist[tp]. Calculate area of rectangle with hist[tp] as smallest bar.
    iii) compute max_area so far and if area > max_area, update max_area
     For hist[tp], the ‘left index’ is previous (previous to tp) item in stack and ‘right index’ is ‘i’ (current index).
  c) push current value (histogram bar) onto max_value stack,
  the index in max_index_stack corresponding to this value will be the start of this rectangle looking-back.
  This should go back farthest to a bar of height >= current-height

3) At the end of iteration, if the stack is not empty, then one by one remove all bars from stack and do step 2b
for every removed bar.

#video explanation
#https://www.youtube.com/watch?v=VNbkzsnllsU

time complexity: O(n^2) in the worst case of monotonically increasing histogram bars where you have to push all elements
 onto the stack. best case
space complexity: O(2n)
"""


def area_largest_rectangle(hist):
    """
    :param
    @param hist: integer list
    :return: area of largest rectangle in histogram
    """
    """input constraint given: histogram bars are always +ve"""
    max_area = 0
    max_index_stack = []
    max_value_stack = []
    temp_index = 0
    for i, e in enumerate(hist):
        if len(max_value_stack) == 0 or e > max_value_stack[-1]:
            max_index_stack.append(i)
            max_value_stack.append(e)

        elif e < max_value_stack[-1]:
            while len(max_value_stack) != 0 and e < max_value_stack[-1]:
                temp_index, max_area = pop_and_compute_area(max_area, max_index_stack, max_value_stack, i)

            max_index_stack.append(temp_index) #keeps the index where this rectangle has to start
            max_value_stack.append(e)

    while len(max_value_stack) != 0:
        temp_index, max_area = pop_and_compute_area(max_area, max_index_stack, max_value_stack, len(hist))
    return max_area


def pop_and_compute_area(max_area, max_index_stack, max_value_stack, curr_index):
    temp_value = max_value_stack.pop()
    temp_index = max_index_stack.pop()
    temp_area = temp_value * (curr_index - temp_index)
    new_max_area = max(temp_area, max_area)
    return temp_index, new_max_area
