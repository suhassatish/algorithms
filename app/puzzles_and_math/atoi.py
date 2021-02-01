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

    summ = 0
    sign = 1
    for i in range(len(s)-1):
        if s[i] in ('-', '+'):
            sign = -1 if s[i] == '-' else 1
            if not s[i+1].isdigit():
                return 0
        else:
            if s[i].isdigit():
                summ = 10 * summ + int(s[i])
            else:
                return summ * sign
    return summ * sign


print(atoi('-3924x8fc')) # -3924
print(atoi('c++')) # 0
print(atoi('++i')) # 0
print(atoi('++1')) # 0


