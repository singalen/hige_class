import unittest
import listxy


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class ListxyTestCase(unittest.TestCase):
    def test_init_simple(self):
        a = listxy.SpatialList([Point(1, 1)])
        self.assertEqual(1, a.max_x)
        seg = a._segment(1, 1)
        self.assertEqual((listxy.SEGMENTS, listxy.SEGMENTS,), seg)
        seg = a._segment(0, 0)
        self.assertEqual((0, 0,), seg)

    def test_init(self):
        a = listxy.SpatialList([Point(x, x) for x in range(200)])
        seg = a._segment(1, 1)
        self.assertEqual((0, 0,), seg)
        seg = a._segment(100, 100)
        self.assertEqual((listxy.SEGMENTS/2, listxy.SEGMENTS/2,), seg)

    def test_get(self):
        a = listxy.SpatialList([Point(x, x) for x in range(200)])
        near44 = a.get_by_distance(4, 4, 2.5)
        self.assertEqual(3, len(near44))

        near44 = a.get_by_distance(4, 4, 2.9)
        self.assertEqual(5, len(near44))

        near0100 = a.get_by_distance(0, 100, 40)
        self.assertEqual(0, len(near0100))

        near_neg = a.get_by_distance(-1, -1, 1)
        self.assertEqual(0, len(near_neg))
