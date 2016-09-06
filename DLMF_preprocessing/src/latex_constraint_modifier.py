
__author__ = 'Kevin Chen'
__status__ = 'Development'

import argparse

CONVERSIONS = {'\\constraint': '{\\bf C}:~',
               '\\substitution': '{\\bf S}:~',
               '\\drmfnote': '{\\bf NOTE}:~',
               '\\drmfname': '{\\bf NAME}:~',
               '\\proof': '{\\bf PROOF}:~',
               '\\mathematicatag': '{\\bf MtT}:~',
               '\\mathematicareference': '{\\bf MtR}:~',
               '\\mapletag': '{\\bf MpT}:~',
               '\\category': '{\\bf CAT}:~'}
TT = ('\\mathematicatag', '\\mapletag')
TEXT = ('\\mathematicareference', '\\category')


def find_surrounding(line, function):
    # (str, str) -> list
    """
    Finds the indices of the beginning and end of a function; this is the main
    function that powers the converter.

    :param line: line with functions that are going to be searched
    :param function: the function you're trying to find the surrounding
                     brackets for
    :returns: positions of opening and ending brackets
    """
    positions = [0, 0]
    positions[0] = line.find(function)

    # Finds the start and end of a function
    count = 0
    for j in range(positions[0] + len(function), len(line) + 1):

        if line[j] in list('([{'):
            count += 1
        if line[j] in list(')]}'):
            count -= 1
        if count == 0:
            positions[1] = j + 1
            break

    return positions


def combine_percent(lines):
    # (list) -> list
    """
    Combines terms with constraints (ones with percent signs) so that replacing
    is easier.

    :param lines: list of all lines
    :return: same list, but groups of constraint terms are combined
    """
    index = 0
    while index < len(lines):
        if len(lines[index]) >= 3 and lines[index][:3] == '%  ' and \
               index > lines.index('\\begin{equation}'):
            if len(lines[index + 1]) != '' and lines[index + 1][0] == '%':
                add = lines.pop(index + 1)
                lines[index] += '\n' + add.replace('%', ' ')
            else:
                lines[index], lines[index + 1] = lines[index + 1], lines[index]
                index += 2
        else:
            index += 1

    return lines


def replace(line):
    # (str) -> str
    """
    Replaces constraints with viewable metadata.

    :param line: line to be converted
    :returns: converted line
    """
    for word in CONVERSIONS:
        for _ in range(line.count(word)):
            pos = find_surrounding(line, word)
            if pos[0] != pos[1]:
                arg = line[pos[0] + len(word) + 1:pos[1] - 1]\
                    .replace('\n', '').replace('    &', ' &')

                # Splits lines if there are any "&".
                if word in TT:
                    arg = ('}$ \\\\[0.2cm]\n   ' + CONVERSIONS[word] +
                           '$\\tt{').join(arg.split('&'))
                if word in TEXT:
                    arg = ('}$ \\\\[0.2cm]\n   ' + CONVERSIONS[word] +
                           '$\\text{').join(arg.split('&'))
                else:
                    arg = ('\\\\[0.2cm]\n   ' + CONVERSIONS[word])\
                        .join(arg.split('&'))

                if (max([line.find(item) for item in CONVERSIONS]) > pos[1] or
                    max([line.find(CONVERSIONS[item]) for
                         item in CONVERSIONS]) > pos[1]):
                    line = line[:pos[0]] + CONVERSIONS[word] + arg + \
                           ' \\\\[0.2cm]' + line[pos[1]:]
                else:
                    line = line[:pos[0]] + CONVERSIONS[word] + arg + \
                           line[pos[1]:]

    return line


def dollarsign(line):
    # (str) -> str
    """
    Changes "$ $" to "${\\displaystyle }$".

    :param line: line to be converted
    :returns: converted line
    """
    count = []
    for index in range(len(line) - 1, 0, -1):
        if line[index] == '$':
            count.insert(0, index)
        if len(count) == 2:
            # This checks to see if there is already a "displaystyle", so it
            # doesn't add a second useless one.
            if line[count[0]:count[0] + 15] != '${\\displaystyle':
                begin = count[0]
                end = count[1]
                line = line[:begin] + '${\\displaystyle ' + \
                    line[begin + 1: end] + '}' + line[end:]
            count = []

    return line


def main(pathr, pathw):
    # (str, str) -> None
    """
    Main function that reads data and calls other functions to process data.

    :param pathr: directory of file to be read from
    :param pathw: directory of file to be written to
    :return: None
    """
    with open(pathr, 'r') as b:
        before = [c.replace('  %', '%') for c in b.read().split('\n')]

    before = combine_percent(before)

    with open(pathw, 'w') as after:
        for line in before:
            if len(line) >= 3 and line[:3] == '%  ' and \
                            before.index(line) > \
                            before.index('\\begin{equation}'):
                line = replace(line)
                line = dollarsign(line)
                line = '\\begin{flushright}\n' + line.replace('%', ' ') + \
                       '\n\\end{flushright}'

            after.write(line + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Receive .tex file with constraints and convert'
                    ' them viewable metadata.')
    parser.add_argument('PATHR', type=str,
                        help='path of input .tex file, with the current'
                             ' directory as the starting point', )
    parser.add_argument('PATHW', type=str,
                        help='path of file to be outputted to, with the'
                             ' current directory as the starting point')
    args = parser.parse_args()

    main(args.PATHR, args.PATHW)
