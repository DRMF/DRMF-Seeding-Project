"""This program begins with an unprocessed LaTeX file and removes parts that are unnecessary for the DLMF."""

import re
import sys

import parentheses
from utilities import (writeout, readin, get_line_lengths,
                       find_line)

EQ_START = r'\\begin{equation}'
EQ_END = r'\\end{equation}'

CASES_START = r'\begin{cases}'
CASES_END = r'\end{cases}'

EQMIX_START = r'\begin{equationmix}'
EQMIX_END = r'\end{equationmix}'

STD_REGEX = r'.*?###open_(\d+)###.*?###close_0###'


def main():
    if len(sys.argv) != 3:

        fname = "../../data/ZE.tex"
        dot_ind = fname.rfind(".") + 1
        ofname = fname[:dot_ind] + "1." + fname[dot_ind:]

    else:

        fname = sys.argv[1]
        ofname = sys.argv[2]

    writeout(ofname, remove_excess(readin(fname)))


def remove_group(name, content):
    """Removes the group bounded by the group name and then curly braces.
    :param content:
    :param name:
    """

    str_pat = name + STD_REGEX
    pattern = re.compile(str_pat, re.DOTALL)

    return pattern.sub(r'', content)


def remove_section(start, end, content):
    """Removes the section or part bounded by start and end.
    :param start:
    :param end:
    :param content:
    """

    str_pat = start + r'.*?(' + end + r')'
    pattern = re.compile(str_pat, re.DOTALL)

    return pattern.sub(r'\1', content)


def remove_begin_end(name, content):
    """Removes a group bound by \\begin{name} and \\end{name}.
    :param name:
    :param content:
    """

    str_pat = r'\\begin{' + name + r'}.*?\\end{' + name + r'}'
    pattern = re.compile(str_pat, re.DOTALL)

    return pattern.sub(r'', content)


def remove_macro(name, content):
    pattern = re.compile(name + "{(.*?)}")
    return pattern.sub(r'\1', content)


def remove_excess(content):
    """Removes the excess pieces from the given content and returns the updated version as a string.
    :param content:
    """
    oldest = content

    start_eq = re.compile(EQ_START)
    end_eq = re.compile(EQ_END)

    updated = _get_preamble()
    old = content
    content = remove_macro(r"\\lxID", content)

    # edit single lines
    # removed unecessary information that caused an error with pdflatex
    pattern = re.compile(r'\\acknowledgements{.*?}\n\n', re.DOTALL)
    content = re.sub(pattern, r'', content)
    content = re.sub(r'\\maketitle', r' ', content)
    content = re.sub(r'\\bibliography{\.\./bib/DLMF}',
                     r'\\bibliographystyle{plain}' + "\n" + r'\\bibliography{/home/hcohl/DRMF/DLMF/DLMF.bib}', content)
    content = re.sub(r'\\acknowledgements{.*?}', r' ', content)
    content = re.sub(r'\{math}', r'{equation}', content)
    content = re.sub(r'\\galleryitem{.*?}{.*?}', r' ', content)
    content = re.sub(r'\\origref{.*?}{.*?}', r' ', content)
    content = re.sub(r'\\onlyelectronic{.*?{.*?}.*?}', r' ', content)
    content = re.sub(r'\\onlyelectronic{.*?}', r' ', content)
    content = re.sub(r'\\printonly{.*?}', r' ', content)
    pattern = re.compile(r'\\onlyprint{.*?}', re.DOTALL)
    content = re.sub(pattern, r' ', content)
    pattern = re.compile(r'\\origref\[.*?\]{.*?}', re.DOTALL)
    content = re.sub(pattern, r'', content)
    content = re.sub(r'\\begin\{electroniconly}', r' ', content)
    content = re.sub(r'\\end\{electroniconly}', r' ', content)
    content = re.sub(r'\\end\{printonly}', r' ', content)
    content = re.sub(r'\\begin\{printonly}', r' ', content)
    content = re.sub(r'\\DLMF\[.*?\]', r' ', content)
    content = re.sub(r'\\author\[.*?\]{.*?}', r' ', content)

    # modify labels, etc
    content = re.sub(r'\\begin\{equation\}\[.*?\]+', r'\\begin{equation}', content, re.DOTALL)

    print(len(old) - len(content))
    old = content

    content = remove_section(r'\\section{Special Notation}', r'\\part', content)
    content = remove_section(r'\\part{Computation}', r'\\bibliographystyle{plain}', content)
    content = remove_section(r'\\part{References}', r'\\bibliographystyle{plain}', content)
    content = remove_section(r'\\section{Graphics}', r'\\section', content)
    content = remove_section(r'\\section{Graphics}', r'\\section', content)
    content = remove_section(r'\\subsection{Graphics}', r'\\subsection', content)
    content = remove_section(r'\\section{Integrals}', r'\\section', content)
    content = remove_section(r'\\subsection{Integrals}', r'\\subsection', content)
    content = remove_section(r'\\section{Physical Applications}', r'\\bibliographystyle{plain}', content)

    print(len(old) - len(content))

    to_join = []
    in_eq = False

    # takes out comment lines first
    for line in content.split("\n"):

        if re.match(EQ_START, line.lstrip()):
            in_eq = True
        if re.match(EQ_END, line.lstrip()):
            in_eq = False

        # if line only consists of % replace with nothing, otherwise don't add back
        if line.lstrip().startswith("%"):
            if line.rstrip().endswith("%"):
                line = ""
            else:
                if not in_eq:
                    continue

        to_join.append(line)

    content = "\n".join(to_join)

    skip_lines = set()

    # remove begin/end groups
    content = remove_begin_end("figuregroup", content)
    content = remove_begin_end("comment", content)
    content = remove_begin_end("figure", content)
    content = remove_begin_end("errata", content)
    content = remove_begin_end("table", content)
    content = remove_begin_end("table", content)

    content = remove_begin_end("%", content)

    content = remove_begin_end("sidebar", content)
    content = parentheses.remove(content, curly=True)

    to_remove = [
        r'\\citet',
        r'\\lxDeclare\[.*?\]',
        r'\\note',
        r'\\origref',
        r'\\lxRefDeclaration',
        r'\\MarkDefn',
        r'\\indexdefn',
        r'\\MarkNotation',
        r'\\affiliation.*?###open_(\d+)###.*?###close_0###',
    ]

    lengths = get_line_lengths(content)
    lines = content.split('\n')

    entering = re.compile(r'\\begin###open_\d###equation###close_\d###')
    exiting = re.compile(r'\\end###open_\d###equation###close_\d###')

    # Find the lines on which equations start and end
    eq_starts = [m.end() for m in entering.finditer(content)]
    eq_ends = [m.start() for m in exiting.finditer(content)]
    start_end_eq = []

    for i in range(len(eq_starts)):
        eq_starts[i] = find_line(eq_starts[i], lengths)
        eq_ends[i] = find_line(eq_ends[i], lengths)
        start_end_eq.append((eq_starts[i], eq_ends[i]))

    if len(eq_starts) != len(eq_ends):
        print 'UNEVEN DISTRIBUTION OF \\begin{equation} and \\end{equation}'
        sys.exit(-1)

    # go through each group and remove it
    for name in to_remove:

        # for each improper name, put it in ###open### and ###closes###
        str_regex = name   # + STD_REGEX    not really necessary to add STD_REGEX, edit if wrong -oksana
        pattern = re.compile(str_regex, re.DOTALL)

        # go through every match, finding start and end
        for match in pattern.finditer(content):

            # for each match of compiled improper name in file

            start = find_line(match.start(), lengths)
            end = find_line(match.end(), lengths)
            dont_skip = False

            # check that element isn't a comment within an equation
            for eq in start_end_eq:

                if eq[0] <= start <= eq[1]:
                    if lines[start - 1].lstrip().startswith('%'):
                        dont_skip = True

            if lines[start - 1].count('$') % 2 != 0:
                # don't skip if only 1 $ on that line so as to avoid causing wrong math_mode ranges
                dont_skip = True

            if not dont_skip:
                skip_lines.update(range(start, end + 1))

            # define items that cannot be at the beginning of any line or be contined in any line
    illegal_starts = [r'\documentclass{DLMF}', r'\thischapter', r'\part{Notation}', r'\begin{equationgroup',
                      r'\end{equationgroup', r'\begin{onecolumn', r'\end{onecolumn']
    illegal_elements = [r'TwoToOneRule', r'OneToTwoRule', r'\citet']

    # various flags that will be useful when going through the lines, in_eq above for comment control
    in_const = False
    in_cases = False

    eqmix_label = ""
    const_str = ""

    lengths = get_line_lengths(content)

    eq_starts = [m.end() for m in start_eq.finditer(content)]
    eq_ends = [m.start() for m in end_eq.finditer(content)]

    start_end_eq = []

    for i in range(len(eq_starts)):
        eq_starts[i] = find_line(eq_starts[i], lengths)
        eq_ends[i] = find_line(eq_ends[i], lengths)
        start_end_eq.append((eq_starts[i], eq_ends[i]))

    eq_counter = None
    in_eqmix = False

    # remove trailing % and whitespace and add to updated - also remove lines that should be skipped
    for lnum, line in enumerate(lines):

        lnum += 1

        # don't add line back if it should be skipped
        if lnum in skip_lines:
            continue

        if re.match(EQ_START, line.lstrip()):
            in_eq = True
        if re.match(EQ_END, line.lstrip()):
            in_eq = False

        # replaces long ###open and close phrases with curly brackets
        line = parentheses.insert(line, curly=True)
        line_checks = [line.lstrip().startswith(start) for start in illegal_starts] + [element in line for element in
                                                                                       illegal_elements]

        # skip current line if it starts with or contains an illegal element
        if any(line_checks):
            # don't remove comments in equations
            if in_eq:
                if not line.lstrip().startswith('%'):
                    continue

            if not in_eq:
                # don't remove if 1 $ in line (causes missing $ error)
                if line.count('$') % 2 == 0:
                    continue

        # no more trailing % characters after cleaned
        cleaned = line.rstrip().rstrip("%").rstrip()

        # line marks the start of an equationmix, set the flag and remove the line
        if EQMIX_START in cleaned:
            in_eqmix = True
            eq_counter = 0
            if re.search('%', cleaned):
                cleaned = cleaned[:cleaned.index('%')]
            eqmix_label = cleaned[cleaned.index(r'\label'):-1] + ".SE"
            continue

        # line marks the end of an equationmix, set the flag and remove the line
        if EQMIX_END in cleaned:
            in_eqmix = False
            eq_counter = None
            eqmix_label = ""
            continue

        # if this line marks the start of an equation, set the flag
        if re.match(EQ_START, cleaned.lstrip()):
            if in_eqmix:
                if '\\end{equation}' in cleaned:
                    # if in eqmix and \end{equation} in line, space the commands, label, and the actual equation
                    if isinstance(eq_counter, int):
                        eq_counter += 1
                        cleaned = cleaned.lstrip()[:16] + eqmix_label + str(eq_counter) + '}\n' + \
                            cleaned[18:cleaned.index('equation}')] + '\n\\end{equation}'
                        cleaned = re.sub(r'\n{2,}', '\n', cleaned)
                else:
                    # just in eqmix, add the command and label only
                    eq_counter += 1
                    cleaned = cleaned.lstrip()[:16] + eqmix_label + str(eq_counter) + '}'
            else:
                # just in eq, add command and label only: make sure no in line comments get added
                if '\\label' not in cleaned:
                    cleaned = cleaned.lstrip() + eqmix_label
                else:
                    cleaned = cleaned.lstrip()[:16] + cleaned[16: 17 + cleaned[16:].index('}')] + eqmix_label
            in_eq = True

        # if this line marks the end of an equation, set the flag
        if re.match(EQ_END, cleaned.lstrip()):
            in_eq = False

        # comment out constraints and replace commas with double commas; we need to build the entire constraint
        # string and then add it back together
        if cleaned.lstrip().startswith(r"\constraint"):
            in_const = True

        # starting a cases statement
        if CASES_START in cleaned:
            in_cases = True

        # ending a cases statement
        if CASES_END in cleaned:
            in_cases = False

        # remove commas, periods, colons, and semi-colons from the end of equations
        if in_eq and not in_const:
            to_strip = ":;,"

            # don't take off trailing commas when in a cases block
            if in_cases:
                to_strip = to_strip[:-1]

            cleaned = cleaned.rstrip(to_strip)

        # we're still in a constraint, replace commas and comment out
        if in_const:

            const_str += cleaned

            # we're done with the constraint, make substitutions
            if cleaned.rstrip().rstrip(".,").endswith("}"):

                const_str = re.sub(r'\$[;,](\s*(?:\$|or))', r'$ &\1', const_str)
                in_const = False

                # constraint ends with two }, put one on next line
                if cleaned.rstrip().endswith("}}"):
                    const_str = const_str[:-1] + "\n}"

                const_lines = []
                split = const_str.split("\n")

                offset = 1

                # account for the case when there are no newlines present
                if len(split) == 1:
                    offset = 0

                    # split multiline constraints back into multiple lines
                for const_line in split[offset:]:

                    # if line is not just a bracket, comment it out
                    if const_line.strip() != "}":
                        const_line = "%" + const_line

                    const_lines.append(const_line)

                updated.extend(const_lines)
                const_str = ""

            const_str += "\n"

            continue

        updated.append(cleaned)

    content = '\n'.join(updated)

    # remove blank lines around begin and end equation
    space_pat = re.compile(r'\\begin\{equation\}(.*?)$\s+$', re.MULTILINE)
    content = space_pat.sub(r'\\begin{equation}\1', content)

    space_pat = re.compile(r'^\s*$\n\\end\{equation\}', re.MULTILINE)
    content = space_pat.sub(r'\\end{equation}', content)

    # remove consecutive blank lines
    content = re.sub(r'(\n){3,}', '\n\n', content)

    print("Final: {0}".format(len(oldest) - len(content)))

    return content


# returns the preamble as a list of it's lines
def _get_preamble():
    preamble = ['\\documentclass{article}', '\\usepackage{amsmath}', '\\usepackage{amsfonts}',
                '\\usepackage{breqn}',
                '\\usepackage{DLMFmath}', '\\usepackage{DRMFfcns}', '', '\\oddsidemargin -0.7cm', '\\textwidth 18.3cm',
                '\\textheight 26.0cm', '\\topmargin -2.0cm', '', '%  \constraint{', '%  \substitution{',
                '%  \drmfnote{', '%  \drmfname{', '']

    return preamble


if __name__ == "__main__":
    main()
