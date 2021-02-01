"""
Your submission will run against only preliminary test cases. Full test cases will run at the end of the day.
There are two kangaroos on an x-axis ready to jump in the positive direction (i.e, toward positive infinity).
The first kangaroo starts at location  and moves at a rate of  meters per jump. The second kangaroo starts at
location  and moves at a rate of  meters per jump. Given the starting locations and movement rates for each kangaroo,
can you determine if they'll ever land at the same location at the same time?

Input Format

A single line of four space-separated integers denoting the respective values of , , , and .

Constraints

Output Format

Print YES if they can land on the same location at the same time; otherwise, print NO.

Note: The two kangaroos must land at the same location after making the same number of jumps.

Sample Input 0

0 3 4 2
Sample Output 0

YES
Explanation 0

The two kangaroos jump through the following sequence of locations:

Thus, the kangaroos meet after  jumps and we print YES.

Sample Input 1

0 2 5 3
Sample Output 1

NO
Explanation 1

The second kangaroo has a starting location that is ahead (further to the right) of the first kangaroo's starting
location (i.e., ). Because the second kangaroo moves at a faster rate (meaning ) and is already ahead of the first
kangaroo, the first kangaroo will never be able to catch up. Thus, we print NO.
"""


def step(x, v):
    n = 0
    while True:
        yield x + n * v
        n += 1


def will_kangaroos_collide(x1, v1, x2, v2):
    if v1 < 1 or v1 > 10000 or v2 < 1 or v2 > 10000 \
        or x1 < 0 or x2 < 0 or x1 > 10000 or x2 > 10000:
        return "NO"
    if (v1 <= v2 and x1 < x2) \
        or (v1 < v2 and x1 <= x2) \
        or (v2 <= v1 and x2 < x1) \
        or (v2 < v1 and x2 <= x1):
        return "NO"
    elif x1 == x2 and v1 == v2:
        return "YES"
    else:
        slower = min(v1, v2)
        if slower == v1:
            slower_step = step(x1, v1)
            faster_step = step(x2, v2)
        else:
            slower_step = step(x2, v2)
            faster_step = step(x1, v1)
        xfast = next(faster_step)
        xslow = next(slower_step)
        while xfast < xslow:
            xfast = next(faster_step)
            xslow = next(slower_step)
            if xfast == xslow:
                return "YES"
        return "NO"


# if __name__ == "__main__":
start1,speed1,start2,speed2 = input().strip().split(' ')
start1,speed1,start2,speed2 = [int(start1),int(speed1),int(start2),int(speed2)]
print(will_kangaroos_collide(start1, speed1, start2, speed2))