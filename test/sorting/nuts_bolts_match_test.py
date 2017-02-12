import unittest
from app.sorting.nuts_bolts_match import match


class MyTest(unittest.TestCase):
    """
    to run stand alone unit test in python
    python -m unittest test_module.TestClass.test_method
    python -m unittest test.sorting.nuts_bolts_match_test.MyTest.test_match
    """
    def test_match(self):
        nuts = [3, 2, 1, 4]
        bolts = [4, 2, 3, 1]

        # output can be in any order
        expected_out = {(1,1), (2,2), (3,3), (4,4)}

        actual_out = match(nuts, bolts)
        self.assertEqual(actual_out, expected_out)
