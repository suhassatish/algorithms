import unittest
from app.recursion.expression_evaluator import is_valid_expr


class MyTest(unittest.TestCase):
    """
    python -m unittest test.recursion.expression_evaluation_test.MyTest.tests
    """
    def tests(self):
        s = [
            #  (input_string, input_target_int, output (is_valid_expr))
            ("234", 4, False),
            ("222", 24, True),  # 22+2 or 2+22
            ("1234", 11, True),
            ("1232537859", 995, True),  # 123 + 2 + 5*3*7 + 85*9
            ("52341", 20, True),
            ("1123", 124, True)
        ]
        for input_str, target, expected_out in s:
            actual_out = is_valid_expr(input_str, target)
            self.assertEqual(actual_out, expected_out)
