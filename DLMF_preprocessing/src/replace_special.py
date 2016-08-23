"""Replace i, e, and \pi with \iunit, \expe, and \cpi respectively. Creates proper spacing for indexes and removes
unnecessary characters."""

import re
import sys

# for compatibility with Python 3
try:
    from itertools import izip
except ImportError:
    izip = zip

import math_mode
import math_function
import parentheses
from utilities import writeout
from utilities import readin


EQ_START = r'\begin{equation}'
EQ_END = r'\end{equation}'

IND_START = r'\index{'

NAME = 0
SEEN = 1

CASES_START = r'\begin{cases}'
CASES_END = r'\end{cases}'

EQMIX_START = r'\begin{equationmix}'
EQMIX_END = r'\end{equationmix}'

STD_REGEX = r'.*?###open_(\d+)###.*?###close_\1###'


def main():
    if len(sys.argv) != 3:

        fname = "../../data/ZE.1.tex"
        ofname = "../../data/ZE.2.tex"

    else:

        fname = sys.argv[1]
        ofname = sys.argv[2]

    # Below: index_str writes to output file, math_string takes output file as input, and change_original
    # writes to the output based on the previous output file

    unchanged_math = math_function.math_string(fname)
    math_string = remove_special(unchanged_math)
    changed_math = math_function.change_original(fname,math_string)
    formatted = math_function.formatting(changed_math)

    writeout(ofname, formatted)


def remove_special(content):
    """Removes the excess pieces from the given content and returns the updated version as a string.
    IN -> list
    OUT -> string"""
    if isinstance(content, str):
        content = content.split('\n')
    counter = 0

    for function in content:

        lines = function.split('\n')

        # various flags that will help us keep track of what elements we are inside of currently
        inside = {
            "constraint": [r'\constraint{', False],
            "substitution": [r'\substitution{', False],
            "drmfnote": [r'\drmfnote{', False],
            "drmfname": [r'\drmfname{', False],
            "proof": [r'\proof{', False]
        }

        in_eq = True

        pi_pat = re.compile(r'(\s*)\\pi(\s*\b|[aeiou])')
        expe_pat = re.compile(r'\b([^\\]?\W*)\s*e\s*\^')

        spaces_pat = re.compile(r' {2,}')
        paren_pat = re.compile(r'\(\s*(.*?)\s*\)')

        dollar_pat = re.compile(r'(?<!\\)\$')

        comment_str = ""

        updated = []
        # go through content and make replacements where necessary
        for lnum, line in enumerate(lines):

            lnum += 1

            # we need to make the replacements in equations
            if in_eq:

                is_comment = line.lstrip().startswith("%")

                line = pi_pat.sub(r'\1\\cpi\2', line)
                line = expe_pat.sub(r'\1\\expe^', line)

                # only check for flags if the line is comment
                if is_comment:

                    # go through each possible flag and see if it should be set
                    for flag, info in inside.iteritems():

                        # name is present in this line, remember that we're in the block
                        if info[NAME] in line:
                            inside[flag][SEEN] = True

                    comment_str += parentheses.remove(line, curly=True, cached=True) + "\n"

                # only try to make replacements if this line isn't a comment
                if not is_comment:

                    line = line.rstrip(".")

                    line = _replace_i(line)

                elif any(info[SEEN] for info in inside.values()):
                    # ^we're in a special block, look for dollar signs to replace "i"s

                    # if we're done with a special block
                    if comment_str.rstrip().endswith("###close_0###"):

                        comment_str = comment_str[:-1]

                        # reset special block flags
                        for flag in inside:
                            inside[flag][SEEN] = False

                        dollar_locs = [match.start() for match in dollar_pat.finditer(comment_str)]
                        locs_iter = iter(dollar_locs)

                        dollar_pairs = [(first, second) for first, second in izip(locs_iter, locs_iter)]
                        # create a list of ranges that are between dollar signs

                        if len(dollar_locs) % 2:
                            print("MISMATCHED $ in:\n{0}".format(comment_str))
                            sys.exit(-1)

                        # replace "i"s within dollar signs
                        for dollar_pair in dollar_pairs:
                            comment_str = comment_str[:dollar_pair[0]] + _replace_i(
                                comment_str[dollar_pair[0]:dollar_pair[1]]) + comment_str[dollar_pair[1]:]

                        comment_lines = parentheses.insert(comment_str, curly=True).split("\n")

                        # comment_lines[-1] = re.sub(r'[.,]}[.,]?', r'}', comment_lines[-1])
                        # ^ removed bc periods/ commas in comment necessary -oksana
                        updated.extend(comment_lines)


                        comment_str = ""
                    continue

            updated.append(line)

        function = '\n'.join(updated)

        # remove consecutive blank lines and blank lines between \index groups
        spaces_pat = re.compile(r'\n{2,}[ ]?\n+')
        function = spaces_pat.sub('\n\n', function)

        function = re.sub(r'\\index{(.*?)}\n\n\\index{(.*?)}', r'\\index{\1}\n\\index{\2}', function)

        content[counter] = function
        counter += 1

    return content

# replaces "i"s as necessary in words
def _replace_i(words):

    text_pat = re.compile(r'\\text{.*?}')

    iloc = words.find("i")

    # go through every occurence of "i" in the content
    while iloc != -1:

        text_bounds = [(match.start(), match.end()) for match in text_pat.finditer(words)]


        # go through all the text lines
        for start, end in text_bounds:

            # if the "i" is in the \text tag, skip it
            if start < iloc < end:

                iloc = words.find("i", end + 1)

                if len(text_bounds) > 1:
                    continue

        surrounding = ""

        # ensure "i" does not occur at the beginning of the string
        if iloc != 0:
            surrounding += words[iloc - 1]

            # ensure "i" does not occur at the end of the line
        if iloc != len(words) - 1:
            surrounding += words[iloc + 1]

        replacement = words[iloc]

        # at least one of the characters surrounding "i" is not alphabetic, we may need to replace
        if not surrounding.isalpha():

            # one (but not both) of the surrounding characters IS alphabetic, may need to replace
            if any(s.isalpha() for s in surrounding):


                if surrounding[1].isalpha():  # character after is alphabetic

                    # make sure we're not starting a macro
                    if surrounding[0] != "\\":
                        replacement = r'\iunit '

            else:
                # neither of the characters surrounding the "i" are alphabetic, replace
                replacement = r'\iunit'


        # print("Surrounding: {0} - replacement made: {1}".format(surrounding, replacement != "i"))
        if iloc != -1:
            words = words[:iloc] + replacement + words[iloc + 1:]
            iloc = words.find("i", iloc + len(replacement))
        else:
            words = words[:iloc] + replacement

    return words


if __name__ == "__main__":
    main()
