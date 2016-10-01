import unittest
from array_min_dist_bw_equals import find_min_distance_bw_equals


class Test(unittest.TestCase):
    def test_cases(self):
        test_cases = [
            #format: n, A, expected_output
            (6, [1, 0, 1, 3, 3, 1], 1),

            #invalid input
            (8, [2, 2], -1),

            (6, [7, 1, 3, 4, 1, 7], 3),

            (5, [-1, -1, -1, -1, -1], 1)
        ]
        for n, A, expected_output in test_cases:
            result = find_min_distance_bw_equals(n, A)
            self.assertEqual(expected_output, result)
