"""
There are 3 types of processors: A, B and C
Type A: 3 tasks in parallel
Type B: 2 tasks in parallel
Type C: 1/2 task
Question: 100 tasks and 100 processors
A simple program to enumerate all valid assignments of 100 tasks to 100 processors
Valid Assignment: use up all 100 processors to process exactly 100 tasks

Question asked at Apple iTunes analytics team phone screen.
"""
# my work:
# [[A * 33 * 3 tasks, 2 * C * 1 task], []
# 3A + 2B + 0.5C such that x + y + z = 100 and
# xT1 + yT2 + zT3 such that m + n + o = 100

# 3T * m of A + 2T * n of B + 0.5T * o of C

# 3mT +  2nT + 0.5To = 100 =>

# 3m + 2n + 0.5o = 100 =>
# 3m + 2n + 0.5 * [100 - (m + n)] = 100

# 3m + 2n + 50 - 0.5m - 0.5n = 100
# 2.5m + 1.5n = 50


# m + n + o = 100
# o = 100 - (m + n)

# 0.5* o should be a whole number => o = even
# (100 - m * 3T)
# 2T* n = (100 - m * 3T)

def find_mn():
    """
    5m + 3n = 100
    """
    out = []
    for m in range(21):  # optimization: given the equation has 5m, we can run loop upto 20 only
        n = (100 - 5*m)/3.0
        if n.is_integer() and 0 <= n <= 100:
            out.append((m, int(n), int(100 - (m + n))))
    return out
    # m = 2, n  = 30, o = 68
    # 2 * 3 + 30 *


if __name__ == '__main__':
    print find_mn()
