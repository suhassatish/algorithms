import unittest
from app.ll_stacks_q.histogram_largest_rectangle import area_largest_rectangle


class MyTest(unittest.TestCase):
    """
    to run stand alone unit test in python
    python -m unittest test_module.TestClass.test_method
    python -m unittest test.longest_common_substring_test.MyTest.test_lcs
    """
    def test_largest_rectangle_in_histogram(self):
        input_list_expected_output_tuples = [
            ([1, 3, 2, 1, 2], 5),
            ([2, 4, 6, 4, 1, 1, 4, 4, 1, 0, 4, 8], 12)
        ]
        for hist, expected_out in input_list_expected_output_tuples:
            actual_out = area_largest_rectangle(hist)
            self.assertEqual(actual_out, expected_out)