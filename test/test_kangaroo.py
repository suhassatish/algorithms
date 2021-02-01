import unittest
from app.binary_search.kangaroo import will_kangaroos_collide


class Test(unittest.TestCase):
    def test_collision(self):
        res = will_kangaroos_collide(0, 4, 2, 2)
        self.assertEqual(res, "YES")

    def test_no_collision(self):
        res = will_kangaroos_collide(0, 3, 1, 1)
        self.assertEqual(res, "NO")