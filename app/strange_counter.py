"""
https://www.hackerrank.com/contests/hourrank-11/challenges/strange-code

Given a strange counter that counts down from 3 to 1 and doubles everytime it reaches 1,
find the value at any given time t.
eg -
time|value
1   |3
2   |2
3   |1

4   |6
5   |5
6   |4
7   |3
8   |2
9   |1

10  |12
11  |11
...
21  |1


v = strange_counter(t)
eg - strange_counter(6) -> returns 4

counter always starts count down from number = 3

constraints:
1 <= t <= 10^12

1 <= t <= 10^5 for 60% score


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