"""
Given in-order and pre-order traversal results of a binary tree (as arrays), write a function to rebuild the tree.
The function should return the root node.

Trivia - Generally speaking, one needs to be given in-order traversal (with either pre or post or level order) as
input, in order to re-construct a binary tree. Without in-order traversal given, its not possible to reconstruct  a tree
without ambiguity, even if all other 3 traversal orders are given. The only exception, is if we know something more
about the tree, like if the binary tree is full and complete, then we can resolve the ambiguity without having to know
the in-order traversal.

Reading pointer -
http://www.geeksforgeeks.org/if-you-are-given-two-traversal-sequences-can-you-construct-the-binary-tree/

Solutions -
http://articles.leetcode.com/construct-binary-tree-from-inorder-and-preorder-postorder-traversal
http://edwardliwashu.blogspot.com/2013/01/construct-binary-tree-from-preorder-and.html
https://www.youtube.com/watch?v=PAYG5WEC1Gs

"""