"""
Given 2 eggs and a 100-floor building, how do you figure out which floor does it
break when dropped from?


d/dx [100/x + (x - 1)] = 0

 100(-1/x^2) + 1 = 0
 x = 10

x = drop from every kth floor

So 1st egg jumps 10 levels, 2nd egg then goes all the way from 10 to 19.
Maximum drops needed = 19

If 1st drop at x
2nd drop at x + (x - 1)
3rd drop at x + (x-1) + (x-2)
nth drop = x + x-1 + x-2 + .... + 3+2+1
which is summation to x = x(x+1)/2 >= 100

Solving for x, you get around 14.

So 1st egg u drop at 14,(+13) 27 (+12), 39 (+11), 50 (+10), 60 (+9), 69, 77, 84, 90, 95, 99, 100
worst case number of drops of 2 eggs = 14.

Previous worst case of 10 jumps = 19.

The worst case was minimized.
As the 1st egg does more work, the 2nd egg does less and as a result, we can rein in the worst case

Generic version of puzzle: N floors and k eggs. Its a classical DP problem.
You can balance the work done between 2 eggs.
"""