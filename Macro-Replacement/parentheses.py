"""Goes through input file, numbers every opening and corresponding closing parenthesis and writes result to output file."""

import sys
import re

_last_val = 0

def remove(input, curly=False, cached=False):
    """Goes through input and replaces any opening and closing parentheses with numbered markers."""
    
    global _last_val

    counter = 0

    #resume from previous count
    if cached:
        counter = _last_val

    updated = ""

    open = "("
    close = ")"

    #if client wants to replace curly braces, adjust accordingly
    if curly:
        open = "{"
        close = "}"

    #go through input and replace parentheses with labels
    for character in input:

        #found an opening parenthesis, replace it with its label
        if character == open:

            character = "###open_{0}###".format(counter)
            counter += 1

        #found a closing parenthesis, replace it with its label
        if character == close:
            counter -= 1

            if counter < 0:
                counter = 0

            character = "###close_{0}###".format(counter)

        updated += character

    _last_val = counter   #store our spot

    return updated

def insert(input, curly=False):
    """Goes through input and replaces any numbered markers with opening and closing parentheses."""

    o_rep = "("
    c_rep = ")" 
    
    #adjust for curly braces
    if curly:
        o_rep = "{"
        c_rep = "}"

    open_pattern = r'###open_\d###'
    close_pattern = r'###close_\d###'

    input = re.sub(open_pattern, o_rep, input)
    input = re.sub(close_pattern, c_rep, input)

    return input