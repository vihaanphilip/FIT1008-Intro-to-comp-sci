"""Unit Testing for Task 1 and 2"""
__author__ = 'Brendon Taylor'
__docformat__ = 'reStructuredText'
__modified__ = '30/05/2020'
__since__ = '22/05/2020'

import unittest
import sys
from hash_table import LinearProbeHashTable
from frequency import Frequency, Rarity


class TestFrequency(unittest.TestCase):
    def setUp(self) -> None:
        self.frequency = Frequency()

    def test_init(self) -> None:
        self.assertEqual(type(self.frequency.hash_table), LinearProbeHashTable)
        self.assertEqual(self.frequency.dictionary.find_word('test'), 1)

    def test_add_file(self) -> None:
        # TODO: Add 2 or more unit tests
        raise NotImplementedError

    def test_rarity(self) -> None:
        # TODO: Add 2 or more unit tests
        raise NotImplementedError


if __name__ == '__main__':
    unittest.main()

