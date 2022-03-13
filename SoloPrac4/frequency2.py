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
        # TODO: Implement this method
        file = open(filename, 'r', encoding="utf-8")
        line = file.readline()
        new_list = []

        for line in file:
            line = line.lower()
            #line = line.strip()
            #line = line.strip(punctuation)
            line = line.split()

            for i in range(len(line)):
                if line[i] != "":
                    line[i] = line[i].strip(punctuation)
                    new_list.append(line[i])

        for i in range(len(new_list)):
            if new_list[i] in self.dictionary.hash_table:
                
                if new_list[i] in self.hash_table:
                    self.hash_table[new_list[i]] = self.hash_table[new_list[i]] + 1
                else:
                    self.hash_table[new_list[i]] = 1

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

        self.quick_sort(rank_list)
        return rank_list

    def partition(self, array: ArrayList, start: int, end: int) -> int:
        mid = (start+end) //2
        pivot = array[mid][1]
        self.swap(array, start, mid)
        boundary = start

        for k in range(start+1, end+1):
            if array[k][1] > pivot:
                boundary += 1           # creates space to move element
                self.swap(array, k, boundary) # swaps the element to the boundary position
        
        self.swap(array, start, boundary)    # swaps the pivot at start with element in boundary
        return boundary


    def swap(self, array, elem1, elem2):
        array[elem1],array[elem2] = array[elem2],array[elem1]

    def quick_sort(self, array: ArrayList) -> None:
        start = 0
        end = len(array)-1
        self.quick_sort_aux(array,start,end)

    def quick_sort_aux(self, array: ArrayList, start: int, end: int) -> None:
        if start < end:
            boundary = self.partition(array, start, end)
            self.quick_sort_aux(array, start, boundary-1)

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
    #print(f.hash_table)
    
    #print(f.max_word[1])
    #print(f.rarity("mary"))



    #hash_tab = str(f.hash_table)
    #hash_tab = hash_tab.split()
    #print(hash_tab)


    test = f.ranking()
    print(test)

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



