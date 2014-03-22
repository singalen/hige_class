# -*- coding: utf-8 -*-

import unittest
import foxcross


class IsCrossesTest(unittest.TestCase):
    def test_1(self):
        a = [
            '.#...',
            '####.',
            '.####',
            '...#.',
            '.....',
        ]
        self.assertTrue(foxcross.is_crosses(a))

    def test_2(self):
        a = [
            '#####',
            '#####',
            '#####',
            '#####',
            '#####',
        ]
        self.assertFalse(foxcross.is_crosses(a))

    def test_3(self):
        a = [
            '.#....',
            '####..',
            '.####.',
            '.#.##.',
            '######',
            '.#..#.',
        ]
        self.assertTrue(foxcross.is_crosses(a))

    def test_4(self):
        a = [
            '.#..#.',
            '######',
            '.####.',
            '.####.',
            '######',
            '.#..#.',
        ]
        self.assertFalse(foxcross.is_crosses(a))

    def test_5(self):
        a = [
            '...',
            '...',
            '...',
        ]
        self.assertTrue(foxcross.is_crosses(a))
