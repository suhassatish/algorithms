"""
A palindromic decomposition of a string S is a decomposition into is substrings such that
all those substrings are valid palindromes. Print out all possible palindromic decompositions
of a given string.

The brute force solution is to enumerate all the substrings. There are nC2 substrings since you
can pick a substring by choosing 2 indices i and j out of n in NC2 ways = n * (n - 1)/2 = O(n^2)
For each substring, you can tell if its a palindrome in O(n) by keeping 2 pointers at its ends
and advancing them towards each other if they point to the same character, until they meet or
cross over. So the total time complexity is O(n^3).

The above thinking is wrong/incomplete, since for the worst case, of all same string like
"aaaa", the palindromic decompositions are every combination of characters, its almost like a
power set. So the time complexity is O(n * 2^n) in the worst case.
a|a|a|a, aa|a|a, aaa|a|, aaaa, aa|aa, a|a|aa, |a|aaa, a|aa|a

We can improve the best case time complexity by checking if prefix is a palindrome for all possible
prefixes, then recursively calling on the suffix only if prefix is a palindrome
"""
import string
from app.recursion.is_palindrome_recursive import is_palindrome


def palindromic_decompositions(s):
    result = []
    _palindromic_decompositions(s, 0, [], result)
    return result


def _palindromic_decompositions(s, index, partial_decomposition, result):
    """
    We partition the string into prefix and suffix.
    Only if prefix is a palindrome, we recursively call the function on the suffix.

    This is similar in structure to the power_set problem.
    :param s:
    :param index:
    :param partial_decomposition:
    :param result:
    :return:
    """
    if index == len(s):
        result.append(list(partial_decomposition))
        return

    for i in range(index + 1, len(s) + 1):
        prefix = s[index:i]
        if is_palindrome(prefix):
            partial_decomposition.append(prefix)
            _palindromic_decompositions(s, i, partial_decomposition, result)
            partial_decomposition.pop()


if __name__ == '__main__':
    print(palindromic_decompositions("abracadabra"))
    # a|b|r|a|c|a|d|a|b|r|a
    # a|b|r|aca|d|a|b|r|a
    # a|b|r|a|c|ada|b|r|a
