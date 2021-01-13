from datetime import datetime
# timestamps of logins in ascending order
timestamps = [
    1416182478,  #EPOCH TIME
    1416182490,
    # ...
]


def has_five_or_more_in_ANY_30_days(timestamps):
    # should return True or False
    for i,time in enumerate(timestamps):
        start_epoch = time
        end_epoch = epoch(start_epoch + '30days')
        count = 1
        for j in range(i+ 1, len(timestamps)):
            if timestamps[j] > end_epoch:
                break
            else:
                count += 1
            if count == 5:
                return True
    return False


def epoch(time_range):
    pass