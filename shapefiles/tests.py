__author__ = 'user'

import unittest
import synonyms


class SynonymsTest(unittest.TestCase):
    def test_all_synonyms_simple(self):
        s = synonyms.Synonyms()
        self.assertEqual(['USA', 'UNITED STATES OF AMERICA', 'U.S.A.'], s.all_synonyms('USA'))
        self.assertEqual(['UKRAINE'], s.all_synonyms('UKRAINE'))

    def test_are_equal_simple(self):
        s = synonyms.Synonyms()
        self.assertTrue(s.are_equal('USA', 'UNITED STATES OF AMERICA'))
        self.assertFalse(s.are_equal('USA', 'UKRAINE'))
        self.assertTrue(s.are_equal('111', '111'))
