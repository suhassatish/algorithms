"""
try to get this in linear time, constant space
"""


def atoi(s):
    """

    :param s: string input
    :return: float
    """
    s.strip()
    # if not s[0].isdigit() and s[0] not in ('+', '-'):
    #     return 0
    # pass

    sum = 0
    sign = 1
    for i in xrange(len(s)-1):
        if s[i] in ('-', '+'):
            sign = -1 if s[i] == '-' else 1
            if not s[i+1].isdigit():
                return 0
        else:
            if s[i].isdigit():
                sum = 10 * sum + int(s[i])
            else:
                return sum * sign
    return sum * sign

print atoi('-3924x8fc') # -3924
print atoi('c++') # 0
print atoi('++i') # 0
print atoi('++1') # 0


