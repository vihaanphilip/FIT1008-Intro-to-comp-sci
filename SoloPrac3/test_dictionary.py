"""Unit Testing for Task 1 and 2"""
__author__ = 'Brendon Taylor'
__docformat__ = 'reStructuredText'
__modified__ = '20/05/2020'
__since__ = '22/05/2020'

import unittest
from hash_table import LinearProbeHashTable
from dictionary import Statistics, Dictionary


def file_len(filename: str) -> int:
    """Calculates the number of lines in a given file"""
    with open(filename, encoding='UTF-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


class TestDictionary(unittest.TestCase):
    DEFAULT_TABLE_SIZE = 250727
    DEFAULT_HASH_BASE = 31
    DEFAULT_TIMEOUT = 10
    FILENAMES = ['english_small.txt', 'english_large.txt', 'french.txt']
    RANDOM_STR = 'FIT1008 is the best subject!'

    def setUp(self) -> None:
        """ Used by our test cases """
        self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)

    def test_init(self) -> None:
        """ Testing type of our table and the length is 0 """
        self.assertEqual(type(self.dictionary.hash_table), LinearProbeHashTable)
        self.assertEqual(len(self.dictionary.hash_table), 0)

    def test_load_dictionary(self) -> None:
        """ Reading a dictionary and ensuring the number of lines matches the number of words
            Also testing the various exceptions are raised correctly """
        for filename in TestDictionary.FILENAMES:
            self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
            words = self.dictionary.load_dictionary(filename)
            lines = file_len(filename)
            self.assertEqual(words, lines, "Number of words should match number of lines")

    def test_add_word(self) -> None:
        """ Testing the ability to add words """
        # TODO: Add your own test cases
        self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)

        # Test 1:
        self.dictionary.add_word("papaya")
        self.assertEqual(len(self.dictionary.hash_table), 1, "Length of table is not increasing")

        # Test 2:
        self.dictionary.add_word("papaya") # word already in hash table so should not be counted
        self.dictionary.add_word("mango")
        self.dictionary.add_word("apple")
        self.dictionary.add_word("orange")
        self.assertEqual(len(self.dictionary.hash_table), 4, "Length of table is not increasing properly or same word added twice")

    
    def test_find_word(self) -> None:
        """ Ensuring both valid and invalid words """
        # TODO: Add your own test cases
        self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
        self.dictionary.add_word("batman")
        self.dictionary.add_word("superman")
        self.dictionary.add_word("flash")

        # Test 1:
        self.assertEqual(self.dictionary.find_word("batman"), True, "Unable to find word which is present in dictionary")
        self.assertEqual(self.dictionary.find_word("BatMan"), True, "Unable to find word which is present in dictionary (case sensitivity)")

        # Test 2:
        self.assertEqual(self.dictionary.find_word("ironman"), False, "Unable to determine whether word is present in dictionary")

    def test_delete_word(self) -> None:
        """ Deleting valid words and ensuring we can't delete invalid words """
        self.dictionary.load_dictionary('english_small.txt')
        table_size = len(self.dictionary.hash_table)
        with self.assertRaises(KeyError):
            self.dictionary.delete_word(TestDictionary.RANDOM_STR)
        self.assertEqual(len(self.dictionary.hash_table), table_size)

        self.dictionary.delete_word('test')
        self.assertEqual(len(self.dictionary.hash_table), table_size - 1)
        
        # TODO: Add your own test cases
        self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
        self.dictionary.add_word("yahoo")
        self.dictionary.add_word("google")
        self.dictionary.add_word("bing")
        table_size = len(self.dictionary.hash_table)
        
        # Test 1:
        self.dictionary.delete_word('yahoo')
        self.assertEqual(len(self.dictionary.hash_table), table_size - 1, "Table size not decreasing properly when deletion occurs")

        #Test 2:
        self.dictionary.delete_word('GooGle')
        self.assertEqual(len(self.dictionary.hash_table), table_size - 2, "Table size not decreasing properly when deletion occurs")

if __name__ == '__main__':
    unittest.main()
