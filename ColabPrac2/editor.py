""" A scaffold for the simple line-oriented text editor a la UNIX ed.
    The scaffold defines class Editor with a few methods for you to implement.
"""

__author__ = "Maria Garcia de la Banda, modified by Ben Di Stefano, Brendon Taylor and Alexey Ignatiev"
__docformat__ = 'reStructuredText'


from os import linesep
from typing import List
from list_adt import ArrayList
from stack_adt import ArrayStack
import sys


class EditorError(Exception):
    """ Simple EditorError exception.
        Should be raised whenever an error occurs. """
    pass


class Editor:
    """ A simple line-oriented text editor.
        An instance of the Editor can be created and run like this:

        .. code-block:: python

            >>> ed = Editor()
            >>> ed.run()
    """

    def __init__(self) -> None:
        """ Object initialiser. """

        # here will be the text lines we are working with
        self.text_lines = ArrayList(40)

        # stack for undoing actions later on
        self.history = ArrayStack()
        self.keep_history = True

    def run(self) -> None:
        """ This is the frontend of the editor, which is basically an infinite
            loop iterating until the user executes the "quit" command.
            Feel free to improve!
        """

        okay = True
        while True:
            cmd = input('' if okay else '? ').strip()
            if cmd == 'quit':
                sys.exit(0)
            else:
                try:
                    self.execute_command(cmd)
                    okay = True
                except EditorError:
                    okay = False

    def execute_command(self, cmd: str) -> None:
        """ Run one command. """
        cmd = cmd.split()
        if cmd:
            if cmd[0] == 'read':
                self.read_filename(cmd[1])
            elif cmd[0] == 'print':
                self.print_num(line_num=cmd[1] if len(cmd) == 2 else None)
            elif cmd[0] == 'delete':
                self.delete_num(cmd[1])
            elif cmd[0] == 'insert':
                lines = []
                while True:
                    line = input()
                    if line == '.':
                        break
                    lines.append(line)
                self.insert_num(cmd[1], lines)
            elif cmd[0] == 'search':
                self.search_string(cmd[1], cmd[2] if len(cmd) == 3 else None)
            elif cmd[0] == 'undo':
                self.undo()
            else:
                raise EditorError('No such command')

    def read_filename(self, file_name):
        """ Read a file into self.text_lines. """
        try:
            f = open(file_name,'r')
        except FileNotFoundError:
            raise EditorError

        file = f.readlines()

        for x in range(len(file)):
            file[x] = file[x].strip("\n")
            file[x] = file[x].strip()

        for i in file:
            self.text_lines.append(i)

        f.close()

    def print_num(self, line_num=None) -> None:
        """ Print a line of text stored in self.text_lines specified by
            the input argument into standard output.
            If line_num is None, print all the lines.
        """
        if line_num == None:
            for i in range(len(self.text_lines)):
                print(self.text_lines[i])

        else:
       
            line_num = int(line_num)
        
            if line_num == 0:
                raise EditorError("line number cannot be 0")

            if line_num > (len(self.text_lines)) or line_num * (-1) > len(self.text_lines):
                raise EditorError


            if line_num > 0:
                print(self.text_lines[line_num-1])
            elif line_num < 0:
                print(self.text_lines[len(self.text_lines) + line_num])



    def delete_num(self, line_num):
        """ Delete a line of text stored in self.text_lines specified by
            the input argument.
        """
        hist = [None] * 3
        line_num = int(line_num)

        # check if line_num == 0, raises error if it is True
        if line_num == 0:
            raise EditorError

        # check if line_num > len(self.text_lines), raises error if it is True
        if line_num > (len(self.text_lines)):
            raise EditorError
        
        try:
            if line_num > 0:
                hist_text = self.text_lines[line_num-1]
                hist_line = line_num
                self.text_lines.delete_at_index(line_num-1)
            elif line_num < 0:
                hist_text = self.text_lines[len(self.text_lines) + line_num]
                hist_line = len(self.text_lines) + line_num + 1
                self.text_lines.delete_at_index(len(self.text_lines) + line_num)
        except IndexError:
            raise EditorError

        if self.keep_history == True:
            hist[0] = "delete"
            hist[1] = hist_text
            hist[2] = hist_line
            self.history.push(hist)

    def insert_num(self, line_num: str, lines: list) -> None:
        """ Insert multiple lines at a given position. The position and
            the lines are specified as input arguments.
        """
        hist = [None] * 3
        line_num = int(line_num)
        
        # check if line_num == 0, raises error if it is True
        if line_num == 0:
            raise EditorError("line number cannot be 0")

        if line_num == -1:
            hist_line = len(self.text_lines) + 1
            hist_count = len(lines)
            for i in range(len(lines)):
                self.text_lines.append(lines[i])
        else:

            # if line_num < -1, convert it to its equivalent positive index
            if line_num < -1:
                line_num = len(self.text_lines) + line_num + 2

            # subtract line_num by 1 as array index start from 0 not 1
            line_num -= 1

            # if line_num > 0 
            if line_num >= 0 and line_num <= (len(self.text_lines)):
                hist_line = len(self.text_lines)
                hist_count = len(lines)
                for i in range(len(lines)-1, -1, -1):
                    self.text_lines.insert(line_num, lines[i])
            #elif line_num > len(self.text_lines):
            #    for i in range(len(lines)):
            #        self.text_lines.append(lines[i])
            else:
                raise EditorError

        if self.keep_history == True:
            hist[0] = "insert"
            hist[1] = hist_line
            hist[2] = hist_count
            self.history.push(hist)

    def search_string(self, query, replace_with=None) -> None:
        """ Search a string in the current text lines.
            Print all text lines that contain the target query if
            no second argument is given. Otherwise, replace the first
            occurrence of the input string (in each text line where 
            it is found) with the second argument.
            Make sure you use self.print_num() for printing and
            self.delete_num() + self.insert_num() for replacement.
        """

        length = len(self.text_lines)


        if replace_with == None:

            # print out all lines which contains query
            for i in range(length):
                if query in self.text_lines[i]:
                    self.print_num(i+1)

        # if second argument is entered, then check for lines which contains
        else:

            query_index = []

            for i in range(length):
                if query in self.text_lines[i]:
                    self.print_num(i+1)
                    query_index.append(i)


            for i in query_index:
                right_str = self.text_lines[i]
                left_str = ""

                while query not in left_str:
                    letter = right_str[0]
                    left_str += letter
                    
                    index = 0
                    while index != (len(right_str)-1) and right_str[index] == right_str[index+1]:
                        left_str += letter
                        index += 1

                    right_str = right_str.lstrip(letter)

                left_str = left_str.rstrip(query)

                new_str = left_str + replace_with + right_str

                #print(left_str) 
                #print(right_str)
                #print(new_str)
                self.delete_num(i+1)
                self.insert_num(i+1, [new_str])

        """
        length = len(self.text_lines)
        new_string = ""
        
        for line in range(length):
            elem = self.text_lines[line]
            if query in elem:
                self.print_num(str(line+1))
    
                if replace_with is not None:
                    self.delete_num(str(line+1))

                    while query not in new_string:
                        new_string += elem[0]
                        elem = elem.lstrip(elem[0]) 
                    
                    #while loop stops after query fully appended in new_string
                    new_string = new_string.rstrip(query)
                    new_line = new_string + replace_with + elem
                    
                    #print(new_string)
                    #print(replace_with)
                    #print(elem)
                    #print(new_line)
                    print(new_line)
                    self.insert_num(str(line+1), new_line)
        """

    def undo(self) -> None:
        """ Undo the previous operation. """
        
        if self.history.is_empty() == True:
            raise EditorError

        # do not keep history when undoing
        self.keep_history = False

        # pop out latest action
        hist = self.history.pop()

        if hist[0] == "delete":
            self.insert_num(hist[2], [hist[1]])
        elif hist[0] == "insert":
            for i in range(hist[2]):
                self.delete_num(hist[1])
        else:
            self.keep_history = True
            raise EditorError
        
        self.keep_history = True

ed = Editor()
ed.run()
#ed.read_filename("small text.txt")
#print(ed.text_lines)
#ed.delete_num(1)
#print(ed.text_lines)
#ed.insert_num(2, "why")
#print(ed.text_lines)



