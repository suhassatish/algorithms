"""
Given a n-ary tree, find its maximum depth.
The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Input: root = [1,null,3,2,4,null,5,6]
     1
  3    2     4
 5 6
Output: 3

Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
        1
2     3       4       5
     6  7     8     9  10
        11    12    13
        14

Output: 5

"""


class Solution(object):
    def maxDepth(self, root):
        """
        :type root: Node
        :rtype: int
        """
        if root is None:
            return 0
        elif root.children == []:
            return 1
        else:
            height = [self.maxDepth(c) for c in root.children]
            return max(height) + 1


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
