import math_mode
import re


def math_string(in_file):
    # Takes input file or string and returns list of strings when in math mode
    try:  # test if file or string
        math_str = open(in_file).read()
    except:
        math_str = in_file
    output = []
    ranges = math_mode.find_math_ranges(math_str)
    for i in ranges:
        new = math_str[i[0]:i[1]]
        output.append(new)
    return output


def change_original(o_file, changed_math_string_list):
    # Places changed string from math mode back into place in the original function
    try:
        o_string = open(o_file).read()
    except:
        o_string = o_file
    math_ranges = math_mode.find_math_ranges(o_string)
    num = 0
    edited = o_string
    # print math_ranges
    for i in math_ranges[::-1]:
        edited = edited[:i[0]] + changed_math_string_list[::-1][num] + edited[i[1]:]
        num += 1
    return edited


def formatting(file_str):
    # Proper spacing for the indexes and gets rid of all non begin{eq end{eq text
    commands = r'\\[a-zA-Z]+'

    updated = []
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

    unnecessary = ['\\begin{align', '\\end{align', '\\index', '\\paragraph', '\\eqref']

    for lnum, line in enumerate(lines):

        lnum += 1

        not_added = not any([element in line for element in unnecessary])
        past_last += len(line) + 1  # + 1 to compensate for \n

        if '\\begin{equation}' in line:
            # Make a blank line between equations
            if '\\end{equation}' in updated[-1]:
                updated.append('')
            in_eq = True
            been_in_eq = True
        if '\\end{equation}' in line:
            updated.append(line.lstrip())
            in_eq = False
            continue

        if in_eq:
            if line != '':
                updated.append(line.lstrip())

        else:
            # not been in eq
            if not been_in_eq:
                # if text line != command
                if re.match(commands, line.lstrip()):
                    if not_added:
                        updated.append(line)
                elif line == '':
                    updated.append(line)
            else:
                # not in eq but already been in eq
                if re.match(section, line.lstrip()) or line == '':
                    updated.append(line)

                if past_last >= ranges[-1][1]:
                    # In section after last eq
                    if re.match(commands, line.lstrip()) or line == '':
                        if not_added:
                            updated.append(line)

        # if this line is an index start storing it,or write it if we're done with the indexes
        if '\\index{' in line:
            in_ind = True
            ind_str += line + "\n"
            # if next line also index, continue storing
            if '\\index{' in lines[lnum]:
                continue

        if in_ind:
            in_ind = False

            # add a preceding newline if one is not already present
            if previous.strip() != '':
                ind_str = "\n" + ind_str

            fullsplit = ind_str.split("\n")
            updated.extend(fullsplit)
            ind_str = ""

        previous = line

    wrote = "\n".join(updated)

    # remove consecutive blank lines and blank lines between \index groups
    spaces_pat = re.compile(r'\n{2,}[ ]?\n+')
    wrote = spaces_pat.sub('\n\n', wrote)
    wrote = re.sub(r'\\index{(.*?)}\n{2,}(?=\\index{(.*?)})', r'\\index{\1}\n', wrote)

    return wrote
