"""
https://www.hackerrank.com/contests/hourrank-11/challenges/strange-code

constraints:
1 <= t <= 10^12

1 <= t <= 10^5 for 60% score

v = strange_counter(t)

counter always starts count down from number = 3
"""
from itertools import count

def strange_counter(t):
    start_value = 3


    time_at_previous_counter_end = 0
    time_at_counter_end = start_value

    for i in count(start=1): #infinite integer counter starting at 0
        if time_at_previous_counter_end <= t <= time_at_counter_end:
            return 1 + time_at_counter_end - t
        time_at_previous_counter_end = time_at_counter_end
        #print("time_at_previous_counter_end = %s" % time_at_previous_counter_end)
        time_at_counter_end += pow(2,i) * start_value
        #print("time_at_counter_end = %s" % time_at_counter_end)

if __name__ == "__main__":
    t = int(raw_input().strip())
    print strange_counter(t)