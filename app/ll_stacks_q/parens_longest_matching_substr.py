"""
Find the length of the longest substring (contiguous) that has matching opening and closing
parentheses. We only need length, not the substring itself. You may assume valid input for this
exercise, ie input string only has parentheses and nothing else.

http://stackoverflow.com/questions/25952326/find-the-length-of-the-longest-valid-parenthesis-sequence-in-a-string-in-on-t
Tricky to find O(N) solution.
"""


def longest_matching_parens(string):
    if string is None or len(string) == 0:
        return 0
    stk = []
    last_matched_index = -1  # this is to handle cases like this "()()()"
    max_len = 0
    for i,e in enumerate(string):
        if e == '(':
            stk.append(i)
        elif e == ')':
            if len(stk) == 0:  # cant pop from empty stack, eg "))" or ")("
                last_matched_index = i
            else:
                pop_index = stk.pop()
                # found a complete valid combo. Calculate max_length

                # eg "()()()"
                if len(stk) == 0:
                    max_len = max(i - last_matched_index, max_len)

                else:  # eg - "((())" at i = 4; stk = [0]
                    max_len = max(i - stk[-1], max_len)
    return max_len

if __name__ == '__main__':
    print longest_matching_parens("((((())(((()")  # (()) = 4
    print longest_matching_parens("((((")  # 0
    print longest_matching_parens("))))")  # 0
    print longest_matching_parens("()()()")  # 6
    print longest_matching_parens("")  # 0
