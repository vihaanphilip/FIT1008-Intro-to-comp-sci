from hash_table import LinearProbeHashTable
from typing import Tuple
import timeit


class Statistics:
    FILES = ['english_large.txt','english_small.txt','french.txt']
    HASH_BASES = [1,27183,250726]
    TABLESIZES = [250727,402221,1000081]
    
    def load_statistics(self, hash_base: int, table_size: int, filename: str, max_time: int) -> Tuple:
        # TODO: Define method
        dict = Dictionary(hash_base, table_size)

        start_time = timeit.default_timer()

        try:
            dict.load_dictionary(filename, max_time)
        except TimeoutError:
            return (len(dict.hash_table), max_time, dict.hash_table.conflict_count, dict.hash_table.probe_total, dict.hash_table.probe_max, dict.hash_table.rehash_count)

        time_taken = timeit.default_timer() - start_time
        return (len(dict.hash_table), time_taken, dict.hash_table.conflict_count, dict.hash_table.probe_total, dict.hash_table.probe_max, dict.hash_table.rehash_count)
        

    def table_load_statistics(self, max_time:int) -> None:
        """
        This method reads files from the file list defined above and creates
        hash tables with specific hash bases and tablesizes mentioned above by
        calling the load statistics method and then loading the statistics
        to a csv file, which is then saved as output_task2.csv

        :param max_time: The maximum time to be given while reading the files
        :raises: None
        :returns: None
        :Best case: TODO: Add complexity
        :Worst case: TODO: Add complexity
        """

        filename = 'output_task2.csv'
        csv_file = open(filename,"w")
        #Adding headers to csv file
        csv_file.write("Hash Base,Table Size,Label,Filename,Word Count,Time,Conflicts,Probe Count,Probe Max,Rehash Count\n")
        
        for i in range(len(Statistics.FILES)):
            for j in range(len(Statistics.FILES)):
                for k in range(len(Statistics.FILES)):
                    data = self.load_statistics(Statistics.HASH_BASES[i], Statistics.TABLESIZES[j],Statistics.FILES[k], max_time)
                    csv_file.write(str(Statistics.HASH_BASES[i]) + "," + str(Statistics.TABLESIZES[j]) + ",")
                    if k == 0:
                        csv_file.write("B = " + str(Statistics.HASH_BASES[i]) + " / " + "TS = " + str(Statistics.TABLESIZES[j]) + ",")
                    else:
                        csv_file.write(",")
                    csv_file.write(Statistics.FILES[k] + "," + str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(data[5]) + "\n")
        csv_file.close()


class Dictionary:
    DEFAULT_ENCODING = 'utf-8'
    def __init__(self, hash_base: int, table_size: int) -> None:
        """
        This method creates a new Hash Table with the given hash base and
        initial table size, and uses it to initialize the instance variable
        self.hash_table

        :complexity: 
        """
        self.hash_table = LinearProbeHashTable(hash_base, table_size)

    def load_dictionary(self, filename: str, time_limit: int = None) -> int:
        """
        This method helps load a dictionary file and reads its contents 
        into a hash table. Each line contains one singular word

        :param filename: The filename of the dictionary file being read
        :param time_limit: The max time on which a TimeoutError is raised
        :raises TimeoutError: If given time limit is exceeded
        :returns: The number of words being read by the function
        :Best Case: TODO: 
        :Worst Case: TODO: 
        """
        start_time = timeit.default_timer()

        words = 0
        with open(filename, 'r', encoding=Dictionary.DEFAULT_ENCODING) as file_read:
            line = file_read.readline()
            while line:
                line = line.strip()
                self.hash_table[line] = 1
                if time_limit is not None and timeit.default_timer() - start_time > time_limit:
                    raise TimeoutError("Exceeded time limit: " + str(time_limit))
                words += 1
                line = file_read.readline()

        return words
    
    
    def add_word(self, word: str) -> None:
        """
        This method adds the given word to the hash table with integer 1 as the 
        associated data. 

        :complexity: Best/Worst case is O(1)
        """
        word = word.strip()
        word = word.lower()
        self.hash_table[word] = 1

    
    def find_word(self, word: str) -> bool:
        """
        This method returns True if the word is in the hash table and False otherwise.

        :complexity: Best/Worst case is O(1)
        """
        word = word.strip()
        word = word.lower()
        return word in self.hash_table

    def delete_word(self, word: str) -> None:
        """
        This method deletes the given word from the hash table.

        :complexity: Best/Worst case is O(1)
        """
        word = word.strip()
        word = word.lower()
        del self.hash_table[word]
    

def process_option(dictionary : Dictionary, method_name: str) -> None:
    """ Helper code for processing menu options."""
    if method_name == 'read_file':
        filename = input('Enter filename: ')
        try:
            dictionary.load_dictionary(filename)
            print('Successfully read file')
        except FileNotFoundError as e:
            print(e)
    else:
        word = input('Enter word: ')
        if method_name == 'add_word':
            dictionary.add_word(word)
            try:
                dictionary.add_word(word)
                print('[{}] {}'.format(word, 'Successfully added'))
            except IndexError as e:
                print('[{}] {}'.format(word, e))
        elif method_name == 'find_word':
            if dictionary.find_word(word):
                print('[{}] {}'.format(word, 'Found in dictionary'))
            else:
                print('[{}] {}'.format(word, 'Not found in dictionary'))
        elif method_name == 'delete_word':
            try:
                dictionary.delete_word(word)
                print('[{}] {}'.format(word, 'Deleted from dictionary'))
            except KeyError:
                print('[{}] {}'.format(word, 'Not found in dictionary'))

def menu(dictionary : Dictionary):
    """ Wrapper for using the dictionary. """
    option = None
    menu_options = {'read_file': 'Read File',
                    'add_word': 'Add Word',
                    'find_word': 'Find Word',
                    'delete_word': 'Delete Word',
                    'exit': 'Exit'}

    exit_option = list(menu_options.keys()).index('exit') + 1

    while option != exit_option:
        print('---------------------')
        opt = 1
        for menu_option in menu_options.values():
            print('{}. {}'.format(opt, menu_option))
            opt += 1
        print('---------------------')
        try:
            option = int(input("Enter option: "))
            if option < 1 or option > exit_option:
                raise ValueError('Option must be between 1 and ' + str(exit_option))
        except ValueError as e:
            print('[{}] {}'.format('menu', e))
        else:
            if option != exit_option:
                process_option(dictionary, list(menu_options.keys())[option - 1])
    print("---------------------")

if __name__ == '__main__':

    """
    dictionary = Dictionary(31, 250727)
    #dictionary = Dictionary(27183, 250727)
    menu(dictionary)
    print("Conflict count: " + str(dictionary.hash_table.conflict_count))
    print("Probe Total: " + str(dictionary.hash_table.probe_total))
    print("Probe Max: " + str(dictionary.hash_table.probe_max))
    print("Rehash Count: " + str(dictionary.hash_table.rehash_count))
    #print(dictionary.hash_table)
    """
    statistics = Statistics()
    statistics.table_load_statistics(10)

