"""
Given a 2D matrix, return an integer
|2|6|5|||
|4|8|6|
|1|2|||
| |7

In m by n grid, traverse along a path collecting max sum of grid_values.

In this problem, if you try to do a greedy algorithm,
it will not find the global maximim.

Recursion is about making local simple options.

Always work out recursion formula first, and then the halting condition.

bp = best_path

1) bp(i,j) = A[i,j]  ;  i == m - 1, j == n-1

2) bp(i,j) = A[i,j] +  bp(i, j+1) ; i == m-1

3) bp(i,j)  = A[i,j] + bp(i+1, j);  j == n -1

4) bp(i,j) = A[i,j] + Max(bp(i,j+1), bp(i+1,j))

Write code in descending order of importance.
In other words, write the most complex or interesting parts first.
Then handle the boring parts (auxillary or helper functions) in the last,
by modularizing it out.

For time and space complexity analysis, always draw the execution tree.


                             (0, 0)
                       (1,0)       (0,1)
                    (2,0),(1,2)  (1,1),(0,2)
Max height of tree = m + n
Therefore, space complexity = O(m+n)

Each frame takes constant time O(1)
Total number of nodes = 2^(n+m) for a full tree

Tree is "full-enough" ie enough number of internal nodes, to say it is 2^(n+m)

Using dynamic programing, time complexity will be O(mn); space complexity will be O(m/n)
There are 2 techniques - 1 is memoization another is bottom-up.
"""