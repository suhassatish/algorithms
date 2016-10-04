"""
Given a weight limit for a knapsack, and a list of items with weights and benefits, find the optimal knapsack
which maximizes the benefit, whilee the total weight being less than the weight limit

https://www.youtube.com/watch?v=ipRGyCcbrGs

eg -
item    0 1 2 3
wt      5 2 8 6
benefit 9 3 1 4

wt limit = 10
soln: best items = 0 + 1 for benefit = 9 + 3 = 12 within a wt of 7
"""


def _find_best_knapsack(remaining_weight, wt_benefit_list, index, optimal_knapsack):
    """
    :param remaining_weight integer
    :param wt_benefit_tuple: list of tuple
    :param index: index of current wt_benefit_list item being processed
    :param optimal_knapsack: a tuple of (int[] knapsack_item_indices, benefit)
    :return:  a tuple of (list[], benefit) where list[] is all the items in the knapsack with total benefit
    """


def find_best_knapsack(weight_limit, wt_benefit_list):
    """

    :param weight_limit: integer
    :param wt_benefit_list: list of tuple with each tuple being (weight, benefit) pair
    :return:
    """
    return _find_best_knapsack(weight_limit, wt_benefit_list, 0, ([],0))