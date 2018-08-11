import unittest
from app.strings.palindromic_substrings import palindromic_substrings as ps


class MyTest(unittest.TestCase):
    """
    to run stand alone unit test in python
    python -m unittest test_module.TestClass.test_method
    python -m unittest test.strings.palindromic_substrings_test.MyTest.test_ps
    """
    def test_ps(self):
        input_output_tuples = [
            ("abcacbbbca"
             , set({"bb", # even-length palindrome
                    "cac", # odd-length palindromes
                    "bcacb",
                    "bbb",
                    "cbbbc",
                    "acbbbca"})),
        ]
        for s1, expected_out in input_output_tuples:
            actual_out = ps(s1)
            self.assertEqual(actual_out, expected_out)