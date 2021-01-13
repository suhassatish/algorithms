"""
Count the total number of structurally unique
 binary search trees that are possible, given the number of nodes.

Strategy: consider that each value could be the root.
 Recursively find the size of the left and right subtrees.


eg - count_trees(1) -> 1
count_trees(2) -> 2
   root   root
   /       \
 child    child

count_trees(3) -> 5
  r            r         r
 / \           \         \
c1 c2          c1        c1
               \         /
               c2       c2
           mirror images of these 2

count_trees(4) -> 14 =
    1 (root.left has 0 children) * 5 (root.right has 3 children) +
    1 (root.left has 1 child) * 2 (root.right has 2 children) +
    2 (root.left has 2 children) * 1 (root.right has 1 child) +
    5 (root.left has 3 children) * 1 (root.right has 0 children)

Intuition here:
https://www.youtube.com/watch?v=UfA_v0VmiDg
recursive relation count(n) = sigma [k = 1:n] count(k - 1) * count( n - k)

code here:
http://cslibrary.stanford.edu/110/BinaryTrees.html


"""


def count_trees(n):
    if n in [0,1]:
        return 1

    else:
        #  there will be one value at the root, with whatever remains
        # on the left and right each forming their own subtrees.
        # Iterate through all the values that could be the root...
        sums = 0
        for k in range(1,n+1):
            left = count_trees(k - 1)
            right = count_trees(n - k)

            # num of possible trees with this root = left * right
            sums += left * right
        return sums

if __name__ == '__main__':
    print count_trees(4)