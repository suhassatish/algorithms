"""

"""
import unittest
from app.recursion.tree_diameter import EdgeWeightedTree


class MyTest(unittest.TestCase):
    """
    to run stand alone unit test in python
    python -m unittest test_module.TestClass.test_method
    python -m unittest test.recursion.tree_diameter_test.MyTest.tests
    """
    def tests(self):
        s = [
            ("{0,0}", 0),  # 1 node no diameter

            #  root
            # 5/
            # C
            ("{0,1,{5,0}}", 5),  # 1-leaf

             #     root
             #      /5
             #  Child1
             #    /4
             #  Child2
             #  /7
             # Child3
            ("{0,1,{5,1,{4,1,{7,0}}}}", 16),  # still 1-leaf

            # The diameter of the first child is the diameter of the tree
              #   root
              #   5/
              #   C1
              #  8/\7
              # C2a C2b
            ("{0,1,{5,2,{8,0},{7,0}}}", 15),

            # The diameter of the last child is the diameter of the tree
     #          root
     #       _____|_____
     #      |1    |1    |1
     #    C1a    C1b    C1c
     #   5/\7    6/\5  10/\9
     # C2a C2b C2c C2d C2e C2f
            ("{0,3,{1,2,{5,0},{7,0}},{1,2,{6,0},{5,0}},{1,2,{10,0},{9,0}}}", 19),

            # diameter is between a leaf in the first child and a leaf in the third child
     #          root
     #       _____|_____
     #      |5    |5    |5
     #    C1a    C1b    C1c
     #   8/\7    9/\8  10/\9
     # C2a C2b C2c C2d C2e C2f
            ("{0,3,{5,2,{8,0},{7,0}},{5,2,{9,0},{8,0}},{5,2,{10,0},{9,0}}}", 29)
        ]
        for tree_str, expected_out in s:
            actual_out = EdgeWeightedTree(tree_str).get_diameter()
            self.assertEqual(actual_out, expected_out)