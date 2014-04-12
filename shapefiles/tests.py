__author__ = 'user'

import unittest
import synonyms


class SynonymsTest(unittest.TestCase):
    def test_all_synonyms_simple(self):
        s = synonyms.Synonyms()
        self.assertEqual(['USA', 'United States of America'], s.all_synonyms('USA'))
        self.assertEqual(['Ukraine'], s.all_synonyms('Ukraine'))

    def test_are_equal_simple(self):
        s = synonyms.Synonyms()
        self.assertTrue(s.are_equal('USA', 'United States of America'))
        self.assertFalse(s.are_equal('USA', 'Ukraine'))
        self.assertTrue(s.are_equal('111', '111'))
