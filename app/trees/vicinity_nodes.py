"""
Given large long tree.
Find K values that are closest in value to the given target, smaller or larger than target value.
Assume BST has a node that contains a pointer to left, right and parent.

Dont want to traverse the whole of the left half of the tree. Can get to target directly.


Look at k-1 on the left and k-1 on the right.

PriorityQ max Heap. Element furthest away, any better than that?
Find closest predecessor to a given node, find closest successor to a given node.


45-min interview breakdown -
comprehension
problem solving abilities
5 mins for examples and approach
15 mins algo dev thru pseudo code
15 mins for coding
10 mins walk through test cases
-----------


"""
