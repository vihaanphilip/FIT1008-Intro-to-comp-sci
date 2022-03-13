from hash_table import LinearProbeHashTable
from dictionary import Dictionary
from list_adt import ArrayList
from enum import Enum
from typing import Tuple
from string import punctuation
import sys

from referential_array import ArrayR


class Rarity(Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    MISSPELT = 3


class Frequency:
    INIT_HASH_BASE = 31
    INIT_TABLE_SIZE = 250727
    def __init__(self, hash_base: int = INIT_HASH_BASE, table_size: int = INIT_TABLE_SIZE) -> None:
        """
        Constructor for the frequency class, creates a dictionary using the English large file
        :param hash_base: Sets the base for the hash table, defaults to the default value mentioned in
        the Linear Probe Hash Table
        :param table_size: Sets the size for the hash table, defaults to the default value mentioned in
        the Linear Probe Hash Table
        """
        self.hash_table = LinearProbeHashTable(hash_base, table_size)
        self.dictionary = Dictionary(hash_base, table_size)
        self.dictionary.load_dictionary('english_large.txt')
        self.max_word = (None, 0)
    
    def add_file(self, filename: str) -> None:
        # TODO: Implement this method
        """
        
        """
        with open(filename, 'r', encoding=Dictionary.DEFAULT_ENCODING) as file:
            line = file.readline()
            while line:
                line = line.split()
                if line != []:
                    for i in range(len(line)):
                        word = line[i]
                        word = word.lower()
                        word = word.strip(punctuation)
                        
                        if self.dictionary.find_word(word) == True:
                            if word in self.hash_table:
                                self.hash_table[word] = self.hash_table[word] + 1

                                if self.hash_table[word] > self.max_word[1]:
                                    self.max_word = (word, self.hash_table[word])

                            else:
                                self.hash_table[word] = 1

                line = file.readline()

    def rarity(self, word: str) -> Rarity:
        # TODO: Implement this method
        """
        """
        if word in self.hash_table:
            count = self.hash_table[word]
            max = self.max_word[1]
            type = None

            if count >= max/100:
                type = 0
            elif count < max/1000:
                type = 2
            elif count < max/100 and count >= max/1000:
                type = 1
        else:
            type = 3

        return(Rarity(type))

    
    def ranking(self) -> ArrayList[tuple]:
        # TODO: Implement this method
        rank_list = ArrayList(len(self.hash_table))
        array = str(self.hash_table)
        array = array.split()

        # Create the Unsorted ArrayList of Tuples
        for i in range(len(self.hash_table)):
            array[i] = array[i].strip(punctuation)
            
            word = ''
            num = ''

            j=0
            while array[i][j] != ',':
                word += array[i][j]
                j+= 1

            for k in range(j+1, len(array[i])):
                num += array[i][k]
            num = int(num)

            add_me = (word, num)
            rank_list.append(add_me)

        self.qsort(rank_list)
        return rank_list

    def qsort(self, array: ArrayList[tuple]) -> None:
        """ QuickSort public interface. """

        #random.seed()
        self._qsort_aux(array, 0, len(array) - 1)

    def _qsort_aux(self, array: ArrayList[tuple], low: int, high: int) -> None:
        """ Actual implementation of QuickSort.
            Sorts a list of elements in-place.
        """

        if low < high:
            boundary = self.partition(array, low, high)
            self._qsort_aux(array, low, boundary-1)
            self._qsort_aux(array, boundary+1, high)
    
    def partition(self, array: ArrayList[tuple], low: int, high: int) -> int:
        """ Randomly selects a pivot element and
                1. moves smaller elements to the left
                2. moves greater elements to the right
            Returns the position of the pivot element.
        """

        # set pivot as mid
        pivot = (low+high)//2

        # TODO
        array[low], array[pivot] = array[pivot], array[low]
        boundary = low

        for k in range(low+1, high+1):
            if array[k][1] > array[low][1]:
                boundary += 1
                array[k], array[boundary] = array[boundary], array[k]

        array[low], array[boundary] = array[boundary], array[low]
        return boundary

def frequency_analysis() -> None:
    sys.setrecursionlimit(10000)
    frequency = Frequency()
    try:
        frequency.add_file('215-0.txt')
    except FileNotFoundError as e:
        print(e)

    if frequency.max_word is not None:
        most_common_words = frequency.ranking()
        
        # Print the top 10 words
        max_rank = 10
        top = 0
        for word, word_frequency in most_common_words:
            print('[{}] {} -> {}'.format(word, word_frequency, frequency.rarity(word)))
            top += 1
            if top >= max_rank:
                break


if __name__ == '__main__':
    #frequency_analysis()
    #sys.setrecursionlimit(100000000)
    
    f = Frequency()
    f.add_file("215-0.txt")
    
    #print(len(f.hash_table))
    #print(f.max_word)
    print(f.hash_table)
    
    #print(f.max_word[1])
    #print(f.rarity("mary"))



    #hash_tab = str(f.hash_table)
    #hash_tab = hash_tab.split()
    #print(hash_tab)


    #test = f.ranking()
    #print(test)

    #qsort(test)
    #print(test)

    #test = ArrayList(20)
    #test.append(('word',4))
    #test.append(('yes',2))
    #test.append(('no',4))
    #test.append(('why',4))
    #test.append(('why',4))
    #test.append(('lol',22))
    #test.append(('no',123))
    #test.append(('yes',105))
    #test.append(('heh',77))
    #test.append(('what',66))
    #test.append(2)
    #print(test[0])

    #f.qsort(test)

    #print(test)



