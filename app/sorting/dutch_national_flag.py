"""
Input = 3 colored balls like string "GBGGRBRG"; output = "RRGGGGBB"
Group them by color, R 1st, then G, then B
Constraint: Do in single pass thru array, not 2 passes, inplace using O(1) memory

One approach is to count the number of balls of each color and pad the strings,
but thats forbidden
"""


def dutch_flag_sort(s):
    """
    Tips: name points r,g,b instead of i,j,k
    Even in matrices, name pointers row, col
    :param s:
    :return:
    """
    if s is None or len(s) <= 1:
        return s
    st = list(s.lower())
    # O(n) = list construction time. This is required since str is immutable
    # Hence str characters cannot be swapped in place

    r = 0
    b = len(st) - 1
    g = 0
    # for g in xrange(len(st)): # for-loop doesnt work here since when g and b pointers cross,
    # it will get messed up and undesirable swaps start; eg 'gbggrbrg' returns 'rgggbbrg'

    while g <= b:  # be careful about including the equality sign, otherwise 1 item will be left out

        if st[g] == 'g':
            g += 1
        elif st[g] == 'r':
            # swap with beginning
            st[r], st[g] = st[g], st[r]
            r += 1
            g += 1
        elif st[g] == 'b':
            st[b], st[g] = st[g], st[b]
            b -= 1
    return ''.join(st)  # converts list back into string


if __name__ == '__main__':
    print dutch_flag_sort("GBGGRBRG")  # rrggggbb
