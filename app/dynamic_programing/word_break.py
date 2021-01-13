"""
Given a string and a set of dictionary words, separate the string into list of valid dictionary
words

example - input_string = applepie
dictionary = ['apple, 'pie']
output = "apple pie"

"""


def word_break_1(input_string, word_set):
    interim_word_list = []
    result_str = ""
    _word_break_1(input_string, word_set, 0, interim_word_list, result_str)
    return result_str


def _word_break_1(input_string, word_set, index, tmp_word_list, result_str):
    """
    This problem is very similar in structure to palindromic decompositions.
    The key is to recognize how to substring when a word is found wrt index and i variables

    For a worst case input like "itsitsitsits" where 'it', 'its', 'sit', 'sits' are all valid words,
    its still an exponential solution.

    This is an experimental solution, that doesn't fully work. There are better dynamic programing
    approaches below.
    :param input_string:
    :param word_set:
    :param index:
    :param tmp_word_list:
    :param result_str:
    :return:
    """
    if index == len(input_string):
        result_str = " ".join([word for word in list(tmp_word_list)])
        return

    for i in range(index + 1, len(input_string) + 1):
        prefix = input_string[index:i]
        print index, tmp_word_list, prefix, result_str
        # O(1) look-up in hash-set vs O(lg n) binary search look-up in sorted_list
        if prefix in word_set:
            tmp_word_list.append(prefix)
            _word_break_1(input_string, word_set, i + 1, tmp_word_list, result_str)
            tmp_word_list.pop()


def word_break(input_string, word_set):
    """
    This approach uses a dynamic_programing array with the word thats formed at the end of each
    index. The following diagram describes it -
      index  words        last_length
    c   0                     -1
    a   1                     -1
    t   2                     3
    s   3   cat               4
    a   4   cats              -1
    n   5                     -1
    d   6                     3,4
    d   7   sand,and          -1
    o   8                     -1
    g   9                     3
            dog

    Full solution described here
    http://www.programcreek.com/2014/03/leetcode-word-break-ii-java/
    It is still an exponential solution to find all decompositions for an input like
    "itsitsitsits" which has dictionary words 'it', 'its', 'sit', 'sits'

    Instead, of above approach, we can find the decompositions of longest words only.
    This is the solution in EPI 17.7 thebedbathandbeyond.com problem
    In 1st pass, we can find for all n^2 (nC2) substrings s[0:i+1] that are dict words and update
    last_length[i] = len(dict_word) if s[0:i+1] is a valid dict word.
    Then if last_length[i] is a dict word we return that and are done.

    You have 2 nested for-loops and each iteration takes time O(n), so total time is O(n^3)
    EPI describes a solution where the innermost loop runs from k - W to k-1 where W = longest
    dictionary word, so that the time complexity reduces to O(n^2 * W)
    :param input_string:
    :param word_set:
    :return:
    """
    last_length = [-1 for i in range(len(input_string))]
    for i in range(len(input_string)):
        if input_string[0:i+1] in word_set:
            last_length[i] = i + 1

        # if last_length[i] = -1, look for j < i st
        # s[0:j+1] is_valid_word && s[j+1:i+1] is_valid_word
        if last_length[i] == -1:
            for j in range(0, i+1):
                if last_length[j] != -1 and input_string[j + 1: i + 1] in word_set:
                    last_length[i] = i - j

    # now get all the decompositions from last_length list.
    decompositions = []
    if last_length[-1] != -1:
        idx = len(input_string) - 1
        while idx >= 0:
            decompositions.append(input_string[idx + 1 - last_length[idx]:idx + 1])
            idx -= last_length[idx]
    decompositions.reverse()
    ret_str = ' '.join([word for word in decompositions])
    return ret_str

if __name__ == '__main__':
    d = {'apple', 'pie'}
    print word_break("applepie", d)  # apple pie

    d = {'its', 'it', 'sits', 'sit'}
    print word_break("itsitsitsits", d)  # its its its its

    d = {'cat', 'cats', 'an', 'and', 'dog', 'sand', 'dogs'}
    print word_break("catsanddogs", d)  # cats and dogs

    d = {'a', 'aaa', 'is', 'name'}
    print word_break("aaaisaname", d)  # aaa is a name
