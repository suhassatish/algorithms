"""
Leet code 680. Valid Palindrome II
https://leetcode.com/problems/valid-palindrome-ii/

Given a non-empty string s, you may delete at most one character. Judge whether you can make it a palindrome.

Example 1:
Input: "aba"
Output: True

Example 2:
Input: "abca"
Output: True
Explanation: You could delete the character 'c'.
"""


def valid_palindrome(s):
    def is_pali_range(i, j):
        return all(s[k] == s[j-k+i] for k in range(i, j))

    for i in range(len(s) / 2):
        if s[i] != s[~i]:
            j = len(s) - 1 - i
            return is_pali_range(i+1, j) or is_pali_range(i, j-1)
    return True

# edge cases - None list(s), empty list(s), duplicate elements
