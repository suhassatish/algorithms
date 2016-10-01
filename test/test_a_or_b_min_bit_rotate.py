import unittest
from a_or_b_min_bit_rotate import find_min_bit_rotation, minimize, hex2bin


class Test(unittest.TestCase):
    def test_find_min_bit_rotation(self):
        test_cases = [
            #format: a, b, c, k, output_tuple_1, output_tuple_2
            ('B9', '40', '5A', 5, '18', '42'),#regression ('', '12')
            ('B9', '40', '5A', 6, '8', '52'), #
            ('B9', '40', '5A', 8, '0', '5A'), #
            ('2B', '9F', '58', 8, '8', '58'), #
            ('2B', '9F', '58', 9, '0', '58'), #
        ]
        for a,b,c,k,out1,out2 in test_cases:
            res1, res2 = find_min_bit_rotation(a,b,c,k)
            self.assertEqual((out1, out2), (res1, res2))

    def test_minimize(self):
        test_cases = [
            #format: a, b, c, k, output_tuple_1, output_tuple_2
            ('08', '58', '58', 1, '0', '58')
            ]
        for a,b,c,k,exp1,exp2 in test_cases:
            res1, res2 = minimize(hex2bin(a), hex2bin(b), c, k)
            self.assertEqual((exp1, exp2), (res1, res2))

    #passes
    def test_minimize_with_dist_1_should_zero_a_b_equals_c(self):
        res1, res2 = minimize('00001000', '01011000', '01011000', 1)
        self.assertEqual(('00000000', '01011000'), (res1, res2))

    #passes
    def test_minimize_with_dist_0_returns_unchanged_a_b(self):
        res1, res2 = minimize('00001000', '01011000', '01011000', 0)
        self.assertEqual(('00001000', '01011000'), (res1, res2))

    #passes
    def test_minimize_with_dist_2_flip_a_b(self):
        res1, res2 = minimize('10001000', '01011000', '11011000', 2)
        self.assertEqual(('00001000', '11011000'), (res1, res2))