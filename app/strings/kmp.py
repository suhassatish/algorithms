"""
https://www.topcoder.com/community/data-science/data-science-tutorials/introduction-to-string
-searching-algorithms/

http://stackoverflow.com/questions/9182651/whats-the-worst-case-complexity-for-kmp-when-the-goal-is-to-find-all-occurrence
The worst-case time complexity of KMP is O(mR + n) to find any pattern in any text since at-most
1 comparison is made on a text character, where m = length of pattern and n = length of text,
R = size of alphabet or total number of unique characters in the pattern

"""


def kmp(txt, pattern):
    """
    http://jakeboxer.com/blog/2009/12/13/the-knuth-morris-pratt-algorithm-in-my-own-words/
    Proper prefixes of Snape - S, Sn, Sna, Snap (atleast 1 short of full word)
    Proper suffixes of Hagrid - d, id, rid, grid, agrid (atleast 1 short of full word)

    Returns True if pattern appears somewhere in text, false otherwise
    We keep a partial-match-table 't' like so -
    pattern  | a | b | a | b | a | b | c | a |
    index    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    value    | 0 | 0 | 1 | 2 | 3 | 4 | 0 | 1 |

    The value is the length of the longest proper_prefix in the (sub)pattern that matches a proper
    suffix in the same (sub)pattern.

    If a partial match of length partial_match_length(pml) is found, & t[pml] > 1,
    then we can skip ahead by
    pml - t[pml - 1]
    :param txt:
    :param pattern:
    :return:
    """
    pass


def naive_match(pattern, text):
    """
    Naive algorithm to find and return starting position of first match
    takes O(p*t) time e.g. for pattern='a'*(p-1)+'b', text='a'*t
    :param pattern: 
    :param text: 
    :return: 
    """
    for start_pos in range(len(text) - len(pattern) + 1):
        match_len = 0
        while pattern[match_len] == text[start_pos + match_len]:
            match_len += 1
            if match_len == len(pattern):
                return start_pos


def kmp_first_match(pattern, text):
    """
    Find and return starting position of first match, or None if no match exists

    Time analysis:
    each iteration of the inner or outer loops increases 2*start_pos + match_len
    this quantity starts at 0 and ends at most at 2*t+p
    so the total number of iterations of both loops is O(t+p)

    :param pattern: 
    :param text: 
    :return: 
    """
    shift = compute_shifts(pattern)
    start_pos = 0
    match_len = 0
    for c in text:
        while match_len >= 0 and pattern[match_len] != c:
            start_pos += shift[match_len]
            match_len -= shift[match_len]
        match_len += 1
        if match_len == len(pattern):
            return start_pos


def kmp_all_matches(pattern, text):
    """
    Slightly more complicated version to return sequence of all matches
    using Python 2.2 generators (yield keyword in place of return).
    Same time analysis as kmp_first_match.

    :param pattern: 
    :param text: 
    :return: 
    """
    shift = compute_shifts(pattern)
    start_pos = 0
    match_len = 0
    for c in text:
        while match_len >= 0 and pattern[match_len] != c:
            start_pos += shift[match_len]
            match_len -= shift[match_len]
        match_len += 1
        if match_len == len(pattern):
            yield start_pos
            start_pos += shift[match_len]
            match_len -= shift[match_len]


def compute_shifts(pattern):
    """
    Construct shift table used in KMP matching

    Time analysis: each iteration of either loop increases shift+pos
    This quantity starts at 0 and ends at most at 2*p
    So total time is O(p).

    :param pattern: 
    :return: 
    """
    shifts = [None] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern) + 1):
        while shift < pos and pattern[pos - 1] != pattern[pos - shift - 1]:
            shift += shifts[pos - shift - 1]
        shifts[pos] = shift
    return shifts


class KmpPrinceton(object):
    """
    Princeton algorithms implements KMP as a discrete-finite-automata state machine as explained
    here
    http://www.cs.princeton.edu/courses/archive/spring11/cos226/demo/53KnuthMorrisPratt.pdf
    """
    def __init__(self, pat):
        self.pat = pat  # pattern to match
        self.r = 256  # radix or the size of the alphabet
        self.m = len(pat)

        # build discrete-finite-automata (DFA) from pattern
        dfa = [[0 for j in xrange(self.m)] for i in xrange(self.r)]
        dfa[ord(pat[0])][0] = 1
        x = 0  # this is the restart state
        for j in xrange(1,self.m):
            for c in xrange(0, self.r):
                dfa[c][j] = dfa[c][x]  # copy mismatch cases

            dfa[ord(pat[j])][j] = j + 1  # set match case
            x = dfa[ord(pat[j])][x]  # update restart state
        self.dfa = dfa

    def search(self, txt):
        """
        Returns the index of the first occurrence of the pattern string in the text string
        :param txt: the text string
        :return: the index of the first occurrence of the pattern string in the text string, N if
        no such match
        """

        # simulate operation of DFA on text
        n = len(txt)
        j = 0
        i = 0
        for i in xrange(n):
            j = self.dfa[ord(txt[i])][j]
            if j >= self.m:
                break

        if j == self.m:
            return i - self.m + 1  # found
        return n  # not found


# print compute_shifts('aabaaab')
# produces [1, 1, 1, 3, 3, 3, 4, 4]


if __name__ == '__main__':
    # print kmp("ABC ABCDAB ABCDABABCDABDE", "ABCDABD")  # True
    # print kmp("SheSells SeaShells On SeaShore", "See")  # False
    for pat, txt in [('abracadabra', 'abacadabrabracabracadabrabrabracad'),  # 14
                     ('rab', 'abacadabrabracabracadabrabrabracad'),  # 8
                     ('bcara', 'abacadabrabracabracadabrabrabracad'),  # 34 (not found)
                     ('rabrabracad', 'abacadabrabracabracadabrabrabracad'),  # 23
                     ('abacad', 'abacadabrabracabracadabrabrabracad')]:  # 0
        kmp = KmpPrinceton(pat)
        print kmp.search(txt)
