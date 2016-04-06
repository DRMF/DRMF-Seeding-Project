"""Goes through input file,
 numbers every opening and corresponding closing parenthesis and writes result to output file."""

import re

_last_val = 0


def remove(text, curly=False, cached=False):
    """Goes through input and replaces any opening and closing parentheses with numbered markers."""

    global _last_val

    counter = 0

    # resume from previous count
    if cached:
        counter = _last_val

    updated = ""

    open_delimiter = "("
    close_delimiter = ")"

    # if client wants to replace curly braces, adjust accordingly
    if curly:
        open_delimiter = "{"
        close_delimiter = "}"

    # go through input and replace parentheses with labels
    for character in text:

        # found an opening parenthesis, replace it with its label
        if character == open_delimiter:
            character = "###open_{0}###".format(counter)
            counter += 1

        # found a closing parenthesis, replace it with its label
        if character == close_delimiter:
            counter -= 1

            if counter < 0:
                counter = 0

            character = "###close_{0}###".format(counter)

        updated += character

    _last_val = counter  # store our spot

    return updated


def insert(text, curly=False):
    """Goes through input and replaces any numbered markers with opening and closing parentheses."""

    o_rep = "("
    c_rep = ")"

    # adjust for curly braces
    if curly:
        o_rep = "{"
        c_rep = "}"

    open_pattern = r'###open_\d###'
    close_pattern = r'###close_\d###'

    text = re.sub(open_pattern, o_rep, text)
    text = re.sub(close_pattern, c_rep, text)

    return text
