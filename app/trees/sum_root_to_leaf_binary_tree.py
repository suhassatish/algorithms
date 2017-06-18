from binary_tree_prototype import BinaryTreeNode


# @include
def sum_root_to_leaf(tree, partial_path_sum=0):
    """
    Given input tree where Each node's value is a binary bit 0 or 1, with a binary number like 1001
    represented with root as MSB and leaf as LSB. Design an algorithm to compute sum of
    binary numbers represented by the root-to-leaf paths.

    Brute-force solution:
    1) Detect all leaves (n.left is None and n.right is None) and store child-parent mapping in hash
    table.
    2) Each leaf-to-root path yields a binary integer. Sum these ints to get result.
    3) Time complexity = O(Ph) where P = number of paths from root to leaf; h = avg height of tree
    4) Space complexity = O(n) for n-nodes

    Optimal solution: Many paths share nodes.
    1) 2 * int(path from root to parent) + curr_node.val
    2) If leaf, return pps.
    3) Else return _recurse(root_to_left_subtree, pps) + _recurse(root_to_right_subtree, pps)
    4) Time complexity = O(n)
    5) Space complexity = O(1) constant memory.
    :param tree:
    :param partial_path_sum:
    :return:
    """
    if not tree:
        return 0

    partial_path_sum = partial_path_sum * 2 + tree.data
    if not tree.left and not tree.right:  # Leaf.
        return partial_path_sum
    # Non-leaf.
    return (sum_root_to_leaf(tree.left, partial_path_sum) +
            sum_root_to_leaf(tree.right, partial_path_sum))
# @exclude


def main():
    #      1
    #    1   0
    #  0    1 0
    root = BinaryTreeNode(1)
    assert sum_root_to_leaf(root) == 1
    root.left = BinaryTreeNode(1)
    assert sum_root_to_leaf(root) == 3
    root.left.left = BinaryTreeNode(0)
    assert sum_root_to_leaf(root) == 6
    root.right = BinaryTreeNode(0)
    assert sum_root_to_leaf(root) == 8
    root.right.left = BinaryTreeNode(1)
    assert sum_root_to_leaf(root) == 11
    root.right.right = BinaryTreeNode(0)
    assert sum_root_to_leaf(root) == 15


if __name__ == '__main__':
    main()
