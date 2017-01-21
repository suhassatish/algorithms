"""
Given a string, find all palindromes among its substrings
eg - input: "abcacbbbca"
output = {"bb", "cac", "bcacb", "bbb", "cbbbc", "acbbbca"}

The brute force solution would be to find
a) all substrings of the string (you can choose a substring by choosing 2 indices i,j such that
substr = str[i:j+1]. Total ways to pick i,j such that 0 <= i,j <= n is nC2 = n!/(2! * (n-2)!) )
= n * (n -1) / 2 = O(n^2)
and for each substring,
b) consider if its a palindrome. (This can be done in 1-pass of 2 pointers i & j
traversing substring from opposite ends until they meet in the middle i.e., in O(n) time)

so its O(n^3)
"""


def palindromic_substrings(str1):
    palset = set()
    for i in xrange(len(str1)):
        add_palindrome(str1, palset, i, i)  # finds odd-length palindromes
        add_palindrome(str1, palset, i, i + 1)  # finds even-length palindromes
    return palset


def add_palindrome(str1, palindrome_set, begin_index, end_index):
    """
    Note on time complexity: for sparse palindrome strings, it is O(n) since the while loop
    quickly terminates in just 1 iteration

    For palindrome-dense strings, it is O(n^2) as potentiall at every position, you can expand
    outwards to the whole string and keep discovering palindromes
    :param str1:
    :param palindrome_set:
    :param begin_index:
    :param end_index:
    :return:
    """
    while begin_index >= 0 and end_index < len(str1) and str1[begin_index] == str1[end_index]:
        if end_index - begin_index > 0:
            palindrome_set.add(str1[begin_index:end_index+1])
        begin_index -= 1
        end_index += 1

# There is also a more complex O(n) algorithm, but getting it and implementing it in an interview
#  will probable take longer than 45 minutes
# https://www.akalin.com/longest-palindrome-linear-time