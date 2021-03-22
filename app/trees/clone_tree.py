"""
Cloning a tree is best done recursively for simpler code. BFS is trickier.
http://crackprogramming.blogspot.com/2012/11/make-copy-of-binary-tree-given-pointer.html
"""


def copy_tree(node):
    if node is None:
        return None

    new_node = Node(node.val)
    new_node.left = copy_tree(node.left)
    new_node.right = copy_tree(node.right)
    return new_node


class Node(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
