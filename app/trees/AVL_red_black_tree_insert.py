"""
AVL is stricter. It says abs(height(left) - height(right)) <= 1
 (better searches)

Red-Black - more lenient, less rotations.
height(longer_side)/height(shorter_side) <=2  (faster inserts)

Splay trees? self-adjusting trees?
https://en.wikipedia.org/wiki/Splay_tree
A splay tree gets rebalanced on new inserts such that frequent items become the root. amortiized O(lg n) for search,
insert, delete but worst case height can degrade to O(n).
"""


def bst_insert(root, val):
    """
    Doesn't handle duplicates. To handle it, just have 2 conditions, no need to explicitly
    handle equality case.
    :param root:
    :param val:
    :return:
    """
    if root is None:
        node = Node(val)
        return node

    if val < root.val:
        root.left = bst_insert(root.left, val)

    elif val > root.val:
        root.right = bst_insert(root.right, val)

    else:
        root.val = val

    return root


class Node(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
