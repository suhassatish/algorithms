"""
Given a weight limit for a knapsack, and a list of items with weights and benefits, find the optimal
knapsack which maximizes the benefit, while the total weight being less than the weight limit.

https://www.youtube.com/watch?v=ipRGyCcbrGs

eg -
item    0 1 2 3
wt      5 2 8 6
benefit 9 3 1 4

wt limit = 10
soln: best items = 0 + 1 for benefit = 9 + 3 = 12 within a wt of 7

EPI Pg 292: 17.6 Knapsack problem
"""
from collections import namedtuple


def _find_best_knapsack(items, rem_wt, index, memoized_value):
    """
    The classical knapsack recurrence relation is given by optimizing value, subject to weight
    restriction. If knapsack has i - 1 items, you have to decide whether or not to put in ith item,

    You can only put it in if wi = weight of ith item < remaining weight `rem_wt`
    If wi < rem_wt:
        max(V[i - 1][w], V[i - 1][w - wi] + value_i)
    else:  # you dont put ith item in
        V[i][w] = V[i - 1][w]

    The value matrix is the memoized_value variable.
    The base case is when index = 0 or rem_wt = 0 when the value becomes 0
    :param items:
    :param rem_wt:
    :param index:
    :param dp:
    :return: The value from memoized_value[index][rem_wt]
    """
    if index < 0 or rem_wt < 0:
        # no item can be chosen
        return 0

    if memoized_value[index][rem_wt] == -1:
        val_without_item = _find_best_knapsack(items, rem_wt, index - 1, memoized_value)
        if items[index].wt < rem_wt:
            # you can add current item without going over capacity
            val_with_item = _find_best_knapsack(
                items, rem_wt - items[index].wt, index - 1, memoized_value) + items[index].val

        else:  # cannot add current item to knapsack due to capacity restrictions
            val_with_item = val_without_item

        memoized_value[index][rem_wt] = max(val_without_item, val_with_item)

    return memoized_value[index][rem_wt]


def find_best_knapsack(items, capacity):
    """

    :param weight_limit: integer
    :param wt_benefit_list: list of tuple with each tuple being (weight, benefit) pair
    :return:
    """
    memoized_value = [[-1 for _ in range(capacity + 1)] for _ in range(len(items))]
    return _find_best_knapsack(items, capacity, len(items) - 1, memoized_value)

if __name__ == '__main__':
    Item = namedtuple('Item', ['wt', 'val'])
    print find_best_knapsack(map(Item._make, [(5, 9), (2, 3), (8, 1), (6, 4)]), 10)  # 12
