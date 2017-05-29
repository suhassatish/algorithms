"""
Implement an iterator over a binary search tree (BST). The iterator interface has 2 methods -
hasNext() and next(). The iterator will be initialized with the root of the BST (can be imbalanced).

hasNext() and next() should run in avg O(1) time and use O(h) memory where h is the height of tree.
       8
     /  \
    3  10
   / \   \
  1  6   14
    / \  /
   4  7 13

Solution: http://www.programcreek.com/2014/04/leetcode-binary-search-tree-iterator-java/
Asked in Cloudera onsite interview by Marcelo Vanzin
"""


class TreeNode(object):
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key


class TreeIterator(object):
    def __init__(self, root_node):
        """
        The trick is to initialize the iterator to the left most node in the BST, so that after
        that, upon calling next(), it can just iterate forwards (through a modified inorder
        traversal using explicit stack).

        :param root_node: this is a TreeNode object, which is the root of a BST for which iterator
        is requested
        :return:
        """
        self.stk = []
        while root_node is not None:
            self.stk.append(root_node)
            root_node = root_node.left

    def has_next(self):
        return len(self.stk) != 0

    def nexxt(self):
        """
        Typo in method name sinxe next is already a builtin key word in python std lib
        :return:
        """
        node = self.stk.pop()
        result = node.val
        if node.right is not None:
            node = node.right
            while node is not None:
                self.stk.append(node)
                node = node.left
        return result
