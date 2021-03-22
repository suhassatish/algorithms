"""
Given the root node of a binary search tree, return the sum of values of all nodes with a value in the range [low, high].

eg 1 -
Input: root = [10,5,15,3,7,null,18], low = 7, high = 15
Output: 32
    10
  5   15
3  7     18

          10
        5    15
      3  7  13  18
     1  6
eg2 -
[6, 10]
output = 23

"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rangeSumBST(self, root: TreeNode, low: int, high: int) -> int:

        def _inorder(node) -> None:
            if node is None:
                return

            if low <= node.val <= high:
                self.sum += node.val

            # optimized solution - tree pruning during dfs, dont go to nodes outside the range
            if low < node.val:
                _inorder(node.left)

            if node.val < high:
                _inorder(node.right)

        self.sum = 0
        _inorder(root)
        return self.sum
