"""
Given a tree, mirror it.
Example input =
   1
 2   3
    4
     5

output =
      1
    3   2
     4
    5

https://stackoverflow.com/questions/9460255/reverse-a-binary-tree-left-to-right


"""


def mirror(root):
    if root is None:
        return
    mirror(root.left)
    mirror(root.right)
    root.left, root.right = root.right, root.left
