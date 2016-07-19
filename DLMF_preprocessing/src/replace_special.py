"""Replace i, e, and \pi with \iunit, \expe, and \cpi respectively."""

__author__ = "Alex Danoff"
__status__ = "Development"

import math_mode
import re
import sys


# for compatibility with Python 3
try:
    from itertools import izip
except ImportError:
    izip = zip

from utilities import writeout
from utilities import readin


def main():
    if len(sys.argv) != 3:

        fname = "ZE.1.tex"
        ofname = "ZE.2.tex"
    else:

        fname = sys.argv[1]
        ofname = sys.argv[2]

    string = open(fname).read()

    writeout(ofname, replace_special(string))


def string_to_list(_line, _list):

    _output = []

    if _list != []:

        for i in range(0, len(_list)):
            if i == 0:

                _output.append(_line[0:_list[i][0]])

            else:

                _output.append(_line[_list[i - 1][1]:_list[i][0]])

            _output.append(_line[_list[i][0]:_list[i][1]])

        if len(_line) != _list[i][1] + 1:

            length = len(_line)
            _output.append(_line[_list[i][1]:length])

    else:
        _output.append(_line)
    return _output


def list_to_string(list):

    output = ""
    for i in list:

        output += i

    return output


def replace_special(string):
    ranges = math_mode.find_math_ranges(string, "DRMF" in string)
    _list = string_to_list(string, ranges)
    for i in range(1, len(_list), 2):

        iloc = _list[i].find("i", 0, len(_list[i]))
        pi_pat = re.compile(r'(\s*)\\pi(\s*\b|[aeiou])')
        expe_pat = re.compile(r'\b([^\\]?\W*)\s*e\s*\^')
        _list[i] = pi_pat.sub(r'\1\\cpi\2', _list[i])
        _list[i] = expe_pat.sub(r'\1\\expe^', _list[i])

        while iloc != -1:
            surrounding = []

            # ensure "i" does not occur at the beginning of the string
            if iloc != 0:

                surrounding.append(_list[i][iloc - 1])
                flag = True
                # ensure "i" does not occur at the end of the line
            if iloc != len(_list[i]) - 1:

                surrounding.append(_list[i][iloc + 1])

            replacement = _list[i][iloc]

            if len(surrounding) == 1:
                if flag:

                    surrounding.append("\n")

                else:

                    surrounding.insert(0, "\n")
            # at least one of the characters surrounding "i" is not alphabetic,
            # we may need to replace
            if not (surrounding[0].isalpha() and surrounding[1].isalpha()):
                # one (but not both) of the surrounding characters IS
                # alphabetic, may need to replace
                if surrounding[0].isalpha != surrounding[1].isalpha and surrounding[
                        0].isalpha() and surrounding[0] in "aeiou":
                    replacement = r'\iunit'

                if surrounding[0].isalpha != surrounding[1].isalpha and not surrounding[
                        0].isalpha and surrounding[0] != "\\":
                    replacement = r'\iunit '

                if surrounding[0].isalpha == surrounding[
                        1].isalpha:  # neither of the characters surrounding the "i" are alphabetic, replace
                    replacement = r'\iunit'

                if (surrounding[0] == " " and surrounding[1] == "}") or (
                        surrounding[0] == "{" and surrounding[1] == " "):
                    replacement = r'\iunit'

            if "\iunit" in replacement and surrounding[1] == " ":
                replacement = r'\iunit'

            # print("Surrounding: {0} - replacement made: {1}".format(surrounding, replacement != "i"))
            _list[i] = _list[i][:iloc] + replacement + _list[i][iloc + 1:]
            if replacement == r'\iunit':
                iloc = _list[i].find("i", iloc + 1, len(_list[i]))
                iloc = _list[i].find("i", iloc + 1, len(_list[i]))
            iloc = _list[i].find("i", iloc + 1, len(_list[i]))
    return list_to_string(_list)

if __name__ == "__main__":
    main()
