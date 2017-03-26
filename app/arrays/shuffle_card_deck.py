"""
Given numbers 1 to N, shuffle the array.

Invariant:
Permutations before the shuffle = independent of permutations after the shuffle.

There are a total of N! permutations. The original order has probability = 1/N!

People get confused with memory-less processes. It means the current state does not affect
the next outcome. Correct shuffling is a memory-less process.
"""


def shuffle(cards_list):
    """
    Draw a card at random from the deck, swap it with first element.
    Then draw a card at random from cards[1:N+1], swap it with 2nd element,
    and so on till N. There are exactly N swaps and hence very deterministic algorithm
    with time complexity O(N)
    :param cards_list:
    :return:
    """
    N = len(cards_list)
    pass
