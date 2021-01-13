"""
find the first and last substring of a string in lexicographically sorted order
where the first letter of each substring is a vowel
and the last letter is a consonant
"""
import re


def findSubstrings(s):
    if not constraint_check_pass(s):
        return None
    filtered_substrs = []
    for i in range(0, len(s)):
        for j in range(i, len(s)):
            if isVowel(s[i]):
                if isVowel(s[j]):
                    continue
                filtered_substrs.append(s[i:j+1])
                #keep track of only the first and last to keep the list small
                filtered_substrs.sort()
                if (len(filtered_substrs) > 2):
                    filtered_substrs = [filtered_substrs[0], filtered_substrs[-1]]

    return filtered_substrs[0], filtered_substrs[-1]


def isVowel(chr):
    return True if chr in ['a', 'e', 'i', 'o', 'u'] else False


def constraint_check_pass(s):
    pattern = re.compile("[^(a-z)]+")
    invalid_chars = pattern.search(s)
    if s is None or len(s) < 3 or len(s) > 5 * 10**5 or invalid_chars:
        return False
    else:
        return True

if __name__ ==  "__main__":
    _s = raw_input()
    first, second = findSubstrings(_s)
    print first
    print second
