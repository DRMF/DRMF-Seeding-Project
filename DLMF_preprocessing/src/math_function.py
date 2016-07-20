import math_mode
import string
import re


def math_string(in_file):
    # Takes input file or string and returns list of strings when in math mode
    try:  # test if file or string
        string = open(in_file).read()
    except:
        string = in_file
    output = []
    ranges = math_mode.find_math_ranges(string)
<<<<<<< HEAD:DLMF_preprocessing/src/math_function.py
    print ranges
=======
>>>>>>> 148bdbf8d7532f66e0bcb24ed0be3d01ee09fa71:AlexDanoff/src/math_function.py
    for i in ranges:
        new = string[i[0]:i[1]]
        output.append(new)
    return output


def change_original(o_file, changed_math_string):
    # Places changed string from math mode back into place in the original function
    try:
        o_string = open(o_file).read()
    except:
        o_string = o_file
    ranges = math_mode.find_math_ranges(o_string)
    num = 0
    edited = o_string
    for i in ranges:
        edited = string.replace(edited, o_string[i[0]:i[1]], changed_math_string[num])
        num += 1
    return edited


def formatting(file_str):
    # Proper spacing for the indexes and gets rid of all non begin{eq end{eq text

    commands = r'\\[a-zA-Z]+'

    updated = []
    IND_START = r'\index\{'
    ind_str = ""
    in_ind = False
    previous = ""

    ranges = math_mode.find_math_ranges(file_str)

    lines = file_str.split('\n')
    in_eq = False
    been_in_eq = False


    section = r'\\[a-zA-Z]*section'

    re.compile(commands)
    re.compile(section)
    past_last = 0

    for line in lines:
        past_last += len(line)

        if '\\begin{equation}' in line:
            in_eq = True
            been_in_eq = False
        if '\\end{equation}' in line:
            updated.append(line)
            in_eq = False
            continue

        if in_eq:
            updated.append(line)

        else:
            # not in eq
            if not been_in_eq:
                # if text line != command
                if re.match(commands, line) or line == '':
                    if '\\paragraph' not in line and '\\acknowledgements' not in line:
                        updated.append(line)
            else:
                # not in eq but already been in eq
                if '\\index' in line or re.match(section,line) or line == '':
                    updated.append(line)

                if past_last > ranges[-1][1]:
                    # In section after last eq
                    if re.match(commands,line) or line == '':
                        if '\\paragraph' not in line:
                            updated.append(line)

        # if this line is an index start storing it,or write it if we're done with the indexes
        if IND_START in line:
            in_ind = True
            ind_str += line + "\n"


        if in_ind:
            in_ind = False

            # add a preceding newline if one is not already present
            if previous.strip() != "":
                ind_str = "\n" + ind_str

            ind_str = ""

        previous = line

    wrote = "\n".join(updated)

    # remove consecutive blank lines and blank lines between \index groups
    spaces_pat = re.compile(r'\n{2,}[ ]?\n+')
    wrote = spaces_pat.sub('\n\n', wrote)
    wrote = re.sub(r'\\index{(.*?)}\n\n\\index{(.*?)}', r'\\index{\1}\n\\index{\2}', wrote)

    return wrote

