"""
Given a string and a set, find the smallest substring that controls the set.
A string 'test', is set to control a set {'t', 'e', 's', 't'},
 if it contains all letters in a set

Example 2- "btabbtgdyafy", set = {'a', 't', 'd'}
                 i   j
output = tgdyafy

Worst case, for 2 members in the set, they appear in the string only once, and at the ends.
So you have to consider the whole set.
"""


def find_controlling_set(input_str, input_set):
    for c in range(len(input_str)):
        _find_controlling_set(input_str, input_set, c, c)
        _find_controlling_set(input_str, input_set, c, c + 1)


def _find_controlling_set(input_str, input_set, start_index, end_index):
    """
    Extending pointer and shrinking pointer.
    Interleaving for loops.
    Interviewer is expecting linear solution.
    This is a common pattern in many questions.
    So familiarity with this pattern is essential.
    :param input_str:
    :param input_set:
    :param start_index:
    :param end_index:
    :return:
    """
    pass


if __name__ == '__main__':
    print(find_controlling_set('btabbtgdyafy', {'a', 't', 'd'}))
