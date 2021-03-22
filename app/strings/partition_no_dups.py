"""
Given a string s, say "abbaghhigfedd", partition it into maximum number of partitions such that the same character
    doesnt appear in multiple partitions, while also maintaining the sort order.
    For example - it should return  [abba, ghhig, f, e, dd]

    Asked by Shruti in IoT Enterprise.
"""


def partition_no_dups(s):
    """
    We'll make 2 passes thru the string. In the first pass, we maintain a hash map of character to (start,end) indexes
    of the character in the string. For the example above,
    {
        a: [0, 3],
        b: [1, 2],
        g: [4,8],
        h: [5,6],
        i: [7],
        f: [9],
        e: [10],
        d: [11, 12]
    }
    :param s: String to partition
    :return: A list of substring partitions of the string such that the same character appears in one and only 1
    partition.
    """
    m = dict()
    for i, e in enumerate(s):
        if e in m:
            start_end_index_list = m[e]

            if len(start_end_index_list) == 1:
            # contains only 1 previous occurrence, we can append the end_index to last_index where we saw this character
                start_end_index_list.append(i)
            else:
            # list already contains [start,end]. Update the end to the last seen.
                start_end_index_list.pop()
                start_end_index_list.append(i)
        else:
            # new character not in map yet
            start_end_index_list = list()
            start_end_index_list.append(i)
            m[e] = start_end_index_list

    # 2nd pass where we prepare our output list
    out = []
    index = 0
    while index < len(s):
        # import ipdb; ipdb.set_trace()
        start_end_lst = m[s[index]]
        if len(start_end_lst) == 1:
            out.append(s[index])
            index += 1
        else:
            start_index, end_index = start_end_lst
            out.append(s[start_index: end_index + 1])
            index = end_index + 1
    return out


def partition_no_dups_v2(s):
    """
    We can further simplify the algorithm by just keeping the index of `last_seen` for
    each character in the map.
    Map m will then look like below -
        {
        a: 3,
        b: 2,
        g: 8,
        h: 6,
        i: 7,
        f: 9,
        e: 10,
        d: 12
    }
    :param s:
    :return:
    """
    m = dict()
    for i, e in enumerate(s):
        m[e] = i

    # 2nd pass where we prepare our output list
    out = []
    index = 0
    while index < len(s):
        last_seen = m[s[index]]
        out.append(s[index: last_seen + 1])
        index = last_seen + 1
    return out


if __name__ == '__main__':
    print(partition_no_dups("abbaghhigfedd"))
    print(partition_no_dups_v2("abbaghhigfedd"))
