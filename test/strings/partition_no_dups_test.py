import unittest
from app.strings.partition_no_dups import partition_no_dups


class MyTest(unittest.TestCase):
    """
        to run stand alone unit test in python
        python -m unittest test_module.TestClass.test_method
        python -m unittest test.strings.partition_no_dups_test.MyTest.test_partition_no_dups
    """
    def test_partition_no_dups(self):
        input_output_tuples = [
            ("abbaghhigfedd", ["abba", "ghhig", "f", "e", "dd"])
        ]
        for s1, expected_out in input_output_tuples:
            actual_out = partition_no_dups(s1)
            self.assertEqual(actual_out, expected_out)