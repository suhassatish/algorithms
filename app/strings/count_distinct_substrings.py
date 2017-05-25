"""
Question asked in Facebook phone screen in Feb 2013.
Given a string, output the total number of distinct substrings.
Ex input -
abababababababababababababababababab

Output = 71
"""


def count_distinct_substrings(s):
    """
    There are nC2 substrings, ie 2 ways to pick i and j in  a string of length n characters
    = n (n - 1)/2 = O(n^2)
    We can put them in a hash_set and find the length of the hash set at the end.
    :param s:
    :return:
    """
    if s is None or len(s) == 0:
        return 0
    st = set()
    for i in xrange(len(s)):
        for j in xrange(i + 1, len(s) + 1):  # since xrange goes 1 less than the end in the range
            substr = s[i:j]
            if substr not in st:
                st.add(substr)
    return len(st)


def count_distinct_substrings_linear(s):
    """
    http://www.geeksforgeeks.org/count-distinct-substrings-string-using-suffix-trie/
    Construct a trie of suffixes (suffix array) in linear time O(n)
    Then, the total number of nodes in the tries gives the total number of distinct substrings.
    :param s:
    :return:
    """
    pass

if __name__ == '__main__':
    print count_distinct_substrings('abababababababababababababababababab')
