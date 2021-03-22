import random
import sys
from .binary_tree_prototype import BinaryTreeNode
# from binary_tree_utils import generate_rand_binary_tree


# @include
def is_binary_tree_bst(tree, low_range=float('-inf'), high_range=float('inf')):
    if not tree:
        return True
    elif not low_range <= tree.data <= high_range:
        return False
    return (is_binary_tree_bst(tree.left, low_range, tree.data) and
            is_binary_tree_bst(tree.right, tree.data, high_range))
# @exclude


def is_binary_tree_bst_alternative(root):
    def inorder_traversal(node):
        if not node:
            return True
        elif not inorder_traversal(node.left):
            return False
        elif prev[0] and prev[0].data > node.data:
            return False
        prev[0] = node
        return inorder_traversal(node.right)
    prev = [None]
    return inorder_traversal(root)


def test():
    #      3
    #    2   5
    #  1    4 6
    tree = BinaryTreeNode(3)
    tree.left = BinaryTreeNode(2)
    tree.left.left = BinaryTreeNode(1)
    tree.right = BinaryTreeNode(5)
    tree.right.left = BinaryTreeNode(4)
    tree.right.right = BinaryTreeNode(6)
    # should output True.
    assert is_binary_tree_bst(tree)
    assert is_binary_tree_bst_alternative(tree)
    #      10
    #    2   5
    #  1    4 6
    tree.data = 10
    # should output False.
    assert not is_binary_tree_bst(tree)
    assert not is_binary_tree_bst_alternative(tree)
    # should output True.
    assert is_binary_tree_bst(None)
    assert is_binary_tree_bst_alternative(None)

    # corner test case when grandchild violates the bst rule but imediate parent-child do not.
    #     3
    #   2    5
    #       2  7
    # other corner cases - all duplicate values
    tree2 = BinaryTreeNode(3)
    tree2.left = BinaryTreeNode(3)
    tree2.right = BinaryTreeNode(5)
    tree2.right.left = BinaryTreeNode(2)
    assert not is_binary_tree_bst(tree)
    assert not is_binary_tree_bst_alternative(tree)


def main():
    test()
    for _ in range(1000):
        n = int(sys.argv[1]) if len(sys.argv) == 2 else random.randint(1, 5)
        # root = generate_rand_binary_tree(n, False)
        # assert is_binary_tree_bst(root) == is_binary_tree_bst_alternative(root)


if __name__ == '__main__':
    # run script from $REPO_ROOT with `python3 -m app.trees.is_binary_tree_a_bst`
    main()
