"""
Array Challenge
Have the function ArrayChallenge(arr) read the array of integers stored in arr which will be in the following format:
[K, r1, r2, r3, ...] where K represents the number of desks in a classroom, and the rest of the integers in the array
will be in sorted order and will represent the desks that are already occupied. All of the desks will be arranged in 2
columns, where desk #1 is at the top left, desk #2 is at the top right, desk #3 is below #1, desk #4 is below #2, etc.
Your program should return the number of ways 2 students can be seated next to each other. This means 1 student is on
the left and 1 student on the right, or 1 student is directly above or below the other student.

For example: if arr is [12, 2, 6, 7, 11] then this classrooms looks like the following picture:



Based on above arrangement of occupied desks, there are a total of 6 ways to seat 2 new students next to each other.
The combinations are: [1, 3], [3, 4], [3, 5], [8, 10], [9, 10], [10, 12]. So for this input your program should
return 6. K will range from 2 to 24 and will always be an even number. After K, the number of occupied desks in the
array can range from 0 to K.

Examples
Input: [6, 4]
Output: 4
Input: [8, 1, 8]
Output: 6
"""


def array_challenge(arr):
    cnt = 0
    desks = []
    for i, e in enumerate(arr):
        if i == 0:
            desks = list(e for e in range(1, arr[0] + 1))
        else:
            desks[e - 1] = 0
    for i, desk_number in enumerate(desks):
        if desk_number == 0:
            continue  # occupied
        elif desk_number % 2 == 1:  # odd desk number check to the right
            if desks[i + 1] != 0:  # right
                cnt += 1

        # both odd and even desks check the row behind them
        if i <= len(desks) - 3 and desks[i + 2] != 0:
            cnt += 1
    return cnt


if __name__ == '__main__':
    print(array_challenge([12, 2, 6, 7, 11]))  # expected = 6
    print(array_challenge([6, 3]))  # 4
    print(array_challenge([6, 6]))  # 5
