"""

"""
from operator import itemgetter


def get_valid_tasks(tasks):
    """
    tasks = [(start1, end1), (start2, end2), ...]
    :param tasks:
    :return: list of selected tasks such that you pick maximum number of tasks
    """
    # pick the one with earliest end time, then pick the next one with the constraint
    # that the next's start time is after the current end_time.
    out = []
    end_sorted = sorted(tasks, key=itemgetter(1))
    i = 0
    while i < len(end_sorted) - 1:
        if len(out) == 0:
            out.append(end_sorted[i])
        else:
            if overlap(out[-1], end_sorted[i]):
                i += 1
                continue
            else:
                # if end_sorted[j][0] >= curr_end:
                out.append(end_sorted[i])
                i += 1

    return out


def overlap(first_interval, second_interval):
    start2 = second_interval[0]
    end1 = first_interval[1]
    if start2 <= end1:
        return True
    else:
        return False


if __name__ == '__main__':
    print(get_valid_tasks([(1,7), (9, 12), (5,11), (8,12), (6,10), (2,3), (1,4), (5,8), (9,12)]))
