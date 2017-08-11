import unittest

from app.sorting.quick_sort_select_rank import qsort


class MyTest(unittest.TestCase):

    def test_qsort(self):
        a = [32, 45, 12, 89, 46, -4]
        b = [-4, 12, 32, 45, 46, 89]
        self.assertEqual(b, qsort(a, 0, len(a)-1))
