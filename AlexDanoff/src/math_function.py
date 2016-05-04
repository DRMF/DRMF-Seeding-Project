import math_mode
import string
from utilities import readin
from utilities import writeout
import re

def math_string(file):
    # Takes input file and returns list of strings when in math mode
    string = open(file).read()
    output = []
    ranges = math_mode.find_math_ranges(string)
    for i in ranges:
        new = string[i[0]:i[1]]
        output.append(new)
    return output


def change_original(o_file, changed_math_string):
    # Places changed string from math mode back into place in the original function
    o_string = open(o_file).read()
    ranges = math_mode.find_math_ranges(o_string)
    num = 0
    edited = o_string
    for i in ranges:
        edited = string.replace(edited, o_string[i[0]:i[1]], changed_math_string[num])
        num += 1
    return edited


def index_spacing(file, out_file):
    used = open(file).read()

    updated = []
    IND_START = r'\index{'
    ind_str = ""
    in_ind = False
    previous = ""
    lines = used.split("\n")

    for line in lines:
        # if this line is an index start storing it, or write it if we're done with the indexes
        if IND_START in line:
            in_ind = True
            ind_str += line + "\n"
            continue

        elif in_ind:
            in_ind = False

            # add a preceding newline if one is not already present
            if previous.strip() != "":
                ind_str = "\n" + ind_str

            fullsplit = ind_str.split("\n")
            updated.extend(fullsplit)
            ind_str = ""
        previous = line
        updated.append(line)

    wrote = "\n".join(updated)

    # remove consecutive blank lines and blank lines between \index groups
    spaces_pat = re.compile(r'\n{2,}[ ]?\n+')
    wrote = spaces_pat.sub('\n\n', wrote)
    wrote = re.sub(r'\\index{(.*?)}\n\n\\index{(.*?)}', r'\\index{\1}\n\\index{\2}', wrote)

    out = open(out_file, 'w')
    out.write(wrote)
    out.close()
    return out
# 4/26, look at chapter 16 and prevent converting the \ApellFiii into \ApellFii\iunit

