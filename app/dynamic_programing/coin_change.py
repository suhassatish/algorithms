"""
Given amount:integer, coin denominations:array
eg - Given 151, coins = [100, 50, 10, 1]. Return [100, 50, 1]

Problem:
1) Give me the coins that add up to the number.
How many ways can we make up the change if there are
unlimited coins?
2) Give me least amount of coins change

Approach:
1) Identify the base case(s)
2) Think if thats the only base case or if there maybe others
eg - if denominations are [100,50,10,2], then base cases are sum = 0, sum = 1
In general, if smallest denomination is s, then base cases are sum = 0 to sum = s-1

3) Discuss what kind of output do you want to return

4) Picture the problem as a tree graph. In this case, each node in tree, will have 4 children,
1 for each denomination.

State assumptions, like for example - coins are sorted in descending order

http://www.geeksforgeeks.org/dynamic-programming-set-7-coin-change/

To estimate time complexity, estimate the total number of solutions (leaf nodes)
and the work that needs to be done to get to each state
In this case its O(amount * len(coins)). Max amount = 151 coins of $1


Alternative versions of the same problem: Given a number,
find the least number of perfect squares that sum up to that number.
Perfect squares are coins here.


"""


def coin_change(amount, denominations):
    """
    This attempts to give change for amount using least number of coins assuming all denominations
    are available
    :param amount:
    :param denominations:
    :return:
    """
    denominations.sort()
    denominations.reverse()
    # coins = [[] for i in range(amount + 1)]
    min_ways = [float('inf') for i in range(amount + 1)]

    #  _coin_change(amount, denominations, min_ways, coins)
    _coin_change(amount, denominations, min_ways)
    return min_ways[amount]


def _coin_change(amount, denominations, min_ways):
    """
    Assuming change of 1,2, 5,10 and an amount of 13, showing the states that we maintain below.
    amount min_ways coins         best_prev_hop_index
     0       1        []             0
     1       1        [1]            0
     2       1        [2]            0
     3       2        [2,1]          2
     4       2        [2,2]          2
     5       1        [5]            0
     6       2        [5,1]          5
     7       2        [5,2]          5
     8       3        [5,2,1]        7
     9       3        [5,2,2]        7
     10      1        [10]           0
     11      2        [10, 1]        10
     12      2        [10,2]         10
     13      3        [10, 2, 1]     12
    Keep an array change[amount] = change for that amount
    :param amount:
    :param denominations:
    :param coins:
    :return:

    Time complexity is O(mV) for 1 solution, exponential time for all solutions
    """
    if amount == 0:
        min_ways[amount] = 1
        # coins[amount] = list()
        return

    if amount < denominations[-1]:
        # if less amount remaining than the minimum change denomination,
        # cant do anything, just return empty change_list
        min_ways[amount] = 0
        # coins[amount] = list()
        return

    for d in denominations:
        if amount - d >= 0:
            min_ways[amount] = min(min_ways[amount - d] + 1, min_ways[amount])

            # prev_coins = coins[amount - d]
            # new_coins = list(prev_coins)
            # coins[amount] = new_coins.append(d)
            _coin_change(amount - d, denominations, min_ways)


def coin_change_iterative(amount, denominations):
    min_coins = [float('inf') for _ in range(amount + 1)]

    # 0 coins required for sum of 0
    min_coins[0] = 0
    denominations.sort()
    denominations.reverse()
    coins = [[] for _ in range(amount + 1)]
    for d in denominations:
        coins[d] = [d]

    for amt in range(amount + 1):
        for coin in denominations:
            if coin <= amt:
                min_coins[amt] = min(min_coins[amt], 1 + min_coins[amt - coin])

                prev_coins = coins[amt - coin]
                new_coins = list(prev_coins)
                new_coins.append(coin)
                if len(coins[amt]) == 0 or \
                    (len(coins[amt]) > 0 and len(coins[amt]) > len(new_coins)):
                    coins[amt] = new_coins

    return -1 if min_coins[amount] == float('inf') else coins[amount]

if __name__ == '__main__':
    print(coin_change_iterative(13, [1, 2, 5, 10]))  # returns [1, 2, 10]
