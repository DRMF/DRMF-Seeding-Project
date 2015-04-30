"""
Provides utility/helper functions for use in other files.
"""

from __future__ import print_function

import re
import sys

#remap input function if necessary
if int(sys.version[0]) >= 3:
    raw_input = input


def debug(function):
    """
    Decorator that starts pdb before calling the function.
    """
    
    def inner(*args, **kwargs):
        
        import pdb
        pdb.set_trace()

        return function(*args, **kwargs)

    return inner

def get_input(prompt, valid=None, list=False, wait=True, preserve_case=False):
    """
    Requests input from stdin until a valid response is given.

    Prompts the user and keeps doing so (with appropriate error
    message) until a valid response is given (i.e. one that is
    specified in valid). If valid is None, any response except
    whitespace or an empty string will be accepted. A space
    will be added after the prompt if one is not present. If
    `list` is specified as True, validity of input will be
    determined character by character, otherwise, it will be
    determined by word. If `wait` is True, will wait for the
    user to press return. Otherwise, will accept first
    typed character as input (using getch).

    For example:::
  
        get_input("enter your name:")

        enter your name: monty
        (returns monty)

        .
        .
        .

        colors = [
            "green",
            "blue",
            "brown",
            "grey"
            "hazel"
        ]

        get_input("enter your eye color:", colors)
        
        enter your eye color: red
        That is not a valid response. Please try again.

        enter your eye color: green
        (returns green)

    """

    input_function = raw_input

    #add quit option and redefine raw_input if we're not waiting
    if not wait:
        valid.add("q")
  
        #returns the result of using getch with a prompt
        def _getch_input(prompt_str):

            print(prompt_str, end="")
            to_return = _getch()
            print("")
            
            return to_return

        input_function = _getch_input

    #add a space after the prompt for readability
    if not prompt.endswith(" "):
        prompt = prompt + " "

        response = input_function(prompt) 
    
    #add spaces and commas to the valid characters for a list
    if list:
        valid.add(",")
        valid.add(" ")

    #keep asking for input until a valid response is given
    while (valid and 
        (any(char not in valid for char in response.lower()) or not list)
        and (response.lower() not in valid or list)
        or response.strip() == ""):

        print("That is not a valid response. Please try again.")
        response = input_function(prompt) 

    to_return = response.lower()
    
    #give response as typed if preserve case specified
    if preserve_case:
        to_return = response

    return to_return

def readin(filename):
    """
    Returns the content of filename as a list of lines.
    """

    return open(filename, "r").read()

def writeout(filename, content, append=False):
    """
    Writes content to file filename.
    """
   
    mode = "w"
    
    #append to the file instead of overwriting
    if append:
        mode = "a"

    #write content
    with open(filename, mode) as out:
        out.write(content)

def get_line_lengths(content):
    """
    Returns a list of the total number of bytes before the end of each line in content.
    """

    lengths = [0]

    total = 0 

    #go through every line
    for i, line in enumerate(content.split("\n")):

        length = len(line)

        total += length + 1    #account for missing newlines
        lengths.append(total)

    return lengths

def unpack_list(first, second, *rest):
    """
    Simulates Python 3's extended iterable unpacking.
      
       Usage:
           my_list = [1,2,3,4]
           
           unpack_list(*my_list)    #returns (1, 2, (3, 4))

    """

    return first, second, rest

def get_last_line(fname):
    """
    Returns the last line in file `fname`.
    """

    all_lines = ""
    last_line = ""

    #get last line
    with open(fname, "r+") as file:
        all_lines = file.read().split("\n")
        last_line = all_lines[-1]        
        del all_lines[-1]

    #if the last line is a number, delete it
    try:

        int(last_line)
        #print("it's a number")      
        #write back all the lines except the last one
        with open(fname, "w+") as file:
            for line in all_lines:
                file.write(line + "\n")    

    except ValueError:
        #print("it's not a number")
        pass

    return last_line

def remove_inner_whitespace(line):
    """
    Removes any repeated spaces from inside `line` (after the first word character) and returns the new string.
    """

    stripped = line.lstrip()

    leading_space = len(line) - len(stripped)
    stripped = re.sub(r' {2,}', ' ', stripped) 

    return ' ' * leading_space + stripped


def find_line(byte, line_lengths):
    """
    Determines which line the character `byte` bytes from the start of the file occurs on using a binary search.
    """
  
    return _find_line_helper(byte, line_lengths, 0, len(line_lengths) - 1)

#uses recursive binary-search-esque algorithm to find what line the given byte is on
def _find_line_helper(byte, line_lengths, start, end):

    mid = (start + end) // 2

    if line_lengths[mid] == byte:
        return mid+1

    next_start = start
    next_end = end

    #target byte is less than mid
    if byte < line_lengths[mid]:

        left = mid - 1

        #target byte between left and mid
        if line_lengths[left] < byte:
            return mid

        next_end = left

    #target byte is between mid and right
    if line_lengths[mid] <= byte:

        right = mid + 1
        
        if line_lengths[right] == byte:
            return right + 1

        #if we're out of bounds, it's on the last possible line
        if right >= end:
           return end

        #target byte between mid and right
        if byte < line_lengths[right]:
            return right

        next_start = right

    return _find_line_helper(byte, line_lengths, next_start, next_end)

class _Getch:
    """
    Gets a single character from standard input.  Does not echo to the screen.
    
    From http://code.activestate.com/recipes/134892/
    By Danny Yoo
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            print(ch, end="")
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

_getch = _Getch()

