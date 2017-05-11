import unittest
from app.strings.longest_common_substring import longest_common_substring as lcs


class MyTest(unittest.TestCase):
    """
    to run stand alone unit test in python
    python -m unittest test_module.TestClass.test_method
    python -m unittest test.longest_common_substring_test.MyTest.test_lcs
    """
    def test_lcs(self):
        input_s1_input_s2_expected_output_tuples = [
            ("suhas", "satsuhasish", "suhas"),
            ("lclc", "clcl", "clc")
        ]
        for s1, s2, expected_out in input_s1_input_s2_expected_output_tuples:
            actual_out = lcs(s1, s2)
            self.assertEqual(actual_out, expected_out)