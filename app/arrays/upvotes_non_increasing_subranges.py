"""
https://www.quora.com/about/challenges

At Quora, we have aggregate graphs that track the number of upvotes we get each day.

As we looked at patterns across windows of certain sizes, we thought about ways to track trends
such as non-decreasing and non-increasing subranges as efficiently as possible.

For this problem, you are given N days of upvote count data, and a fixed window size K.
For each window of K days, from left to right, find the number of non-decreasing subranges
within the window minus the number of non-increasing subranges within the window.

A window of days is defined as contiguous range of days. Thus, there are exactly  windows
where this metric needs to be computed. A non-decreasing subrange is defined as a
contiguous range of indices , , where each element is at least as large as the previous element.
A non-increasing subrange is similarly defined, except each element is at least as large as the
next. There are up to  of these respective subranges within a window, so the metric is bounded by .

Constraints
1 <= N <= 100k days
1 <= K <= N days

there are N - K + 1 windows of length K in a sequence of length N
in a sequence of length K, there are K * (K-1) /2 sub-ranges in all

Input Format

Line 1: Two integers,  and

Line 2:  positive integers of upvote counts, each integer less than or equal to

Output Format

Line 1..:  integers, one integer for each window's result on each line

Sample Input

5 3
1 2 3 1 1
Sample Output

3
0
-2
Explanation

For the first window of [1, 2, 3], there are 3 non-decreasing subranges and 0 non-increasing,
 so the answer is 3. For the second window of [2, 3, 1], there is 1 non-decreasing subrange
 and 1 non-increasing, so the answer is 0. For the third window of [3, 1, 1],
 there is 1 non-decreasing subrange and 3 non-increasing, so the answer is -2.
"""
from itertools import islice


def get_non_dec_non_inc_trend(n, k, arr):
    if not input_constraints_pass(n, k, arr):
        print("failed on input_constraints check")
        return None
    trend_for_all_windows = []
    for window in range(0, n-k+1):
        value = get_nd_minus_ni(arr[window:window+k])
        trend_for_all_windows.append(value)
    return trend_for_all_windows


def get_nd_minus_ni(arr):
    nd = total_non_decreasing_subranges(arr)
    ni = total_non_increasing_subranges(arr)
    return nd - ni


def total_non_decreasing_subranges(arr):
    iterator = range(0, len(arr)).__iter__()
    total_non_dec_subranges = 0
    for current_index in iterator:
        l = length_of_longest_non_decreasing_seq_at(current_index, arr)
        total_non_dec_subranges += l*(l-1)/2
        if l == 1:
            continue
        else:
            consume(iterator, l-1)
    return total_non_dec_subranges


def length_of_longest_non_decreasing_seq_at(start_index, arr):
    length = 1
    for index in range(start_index, len(arr)-1):
        if arr[index] <= arr[index+1]:
            length += 1
        else:
            break
    return length


def total_non_increasing_subranges(arr):
    iterator = range(0, len(arr)).__iter__()
    total_non_inc_subranges = 0
    for current_index in iterator:
        l = length_of_longest_non_increasing_seq_at(current_index, arr)
        total_non_inc_subranges += l*(l-1)/2
        if l == 1:
            continue
        else:
            consume(iterator, l-1)
    return total_non_inc_subranges


def length_of_longest_non_increasing_seq_at(start_index, arr):
    length = 1
    for index in range(start_index, len(arr)-1):
        if arr[index] >= arr[index+1]:
            length += 1
        else:
            break
    return length


def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a list
        list(iterator)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def input_constraints_pass(n, k, arr):
    if n < 1 or n > 1e5:
        return False
    if k < 1 or k > n:
        return False
    if len(filter(non_positive_or_more_than_billion, arr)) > 0:
        return False
    return True


def non_positive_or_more_than_billion(element):
    return element <= 0 or element > 1e9

if __name__ == "__main__":
    input_n, input_k = map(int, input().strip().split(' '))
    input_array = map(int, input().strip().split(' '))
    out = get_non_dec_non_inc_trend(input_n, input_k, input_array)
    if out is not None:
        for i in out:
            print(i)
