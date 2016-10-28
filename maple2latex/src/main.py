#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

import os
from translator import MapleEquation, LatexEquation

TABLE = dict()  # stores meaning of folder names
with open("maple2latex/data/section_names") as name_info:
    for line in name_info.read().split("\n"):
        if line != "" and "%" not in line:
            key, value = line.split(" : ")
            TABLE[key] = value

FILES = [
    "bessel", "modbessel",
    "confluent", "confluentlimit", "kummer", "parabolic", "whittaker",
    "apery", "archimedes", "catalan", "delian", "eulersconstant", "eulersnumber", "goldenratio", "gompertz",
    "naturallogarithm", "powerandroot", "pythagoras", "rabbit", "theodorus", "zeta2", "zeta4",
    "arccos", "arccosh", "arcsin", "arcsinh", "arctan", "arctanh", "cos", "cosh", "coth",
    "exp", "ln", "pow", "sin", "sinh", "tan", "tanh",
    "comperror", "error", "fresnel", "repint",
    "expintegrals", "related",
    "binet", "incompletegamma", "polygamma", "tetragamma", "trigamma",
    "hypergeometric",
    "qhyper",
    "beta_f_t", "gamma_chisquare", "normal", "repeated"
]  # files to be translated


class MapleFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.formulae = self.obtain_formulae()

    def obtain_formulae(self):
        contents = open(self.filename).read()

        return [MapleEquation(piece.split("\n")) for piece in contents.split("create(")
                if "):" in piece or ");" in piece]

    def __str__(self):
        return "MapleFile of " + self.filename


def get_sections_data(dirs, root_depth=0):
    # type: (list(, int)) -> dict
    """Obtain data from the functions/ directory."""
    sections = dict()

    for info in dirs:  # search through directories
        depth = info[0].count("/")

        if depth == root_depth:  # section
            section = TABLE[info[0].split("/")[-1]]
            sections[section] = dict()

            for file_name in info[2]:
                folder = ''.join(file_name.split(".")[:-1])
                if folder in FILES:
                    # generate equation code, sorted by equation number
                    subsection = TABLE[folder]
                    formulae = map(LatexEquation.from_maple, MapleFile(info[0] + "/" + file_name).formulae)
                    formulae = sorted(formulae, key=LatexEquation.get_sortable_label)

                    repr_label = formulae[len(formulae) / 2].label

                    if subsection in sections[section]:
                        sections[section][subsection][1] += "\n".join(map(str, formulae))
                    else:
                        sections[section][subsection] = [repr_label, "\n".join(map(str, formulae))]

    return sections


def translate_files(root_directory, output_file):
    # type: ()
    """Generates and writes the results of traversing the root directory, and translating all files in FILES."""

    root_depth = len(root_directory.split("/"))

    dirs = [d for d in os.walk(root_directory) if d[0].count("/") == root_depth]

    sections = get_sections_data(dirs, root_depth=root_depth)

    # generate subsection headers
    for section, subsections in sections.iteritems():
        keys = sorted(subsections.keys(), key=lambda x: subsections[x][0])

        text = ""
        for subsection in keys:
            text += "\n\\subsection{" + subsection + "}\n"
            text += subsections[subsection][1]

        sections[section] = text

    # generate section headers
    result = ""
    for section, section_data in sections.iteritems():
        result += "\\section{" + section + "}\n" + section_data + "\n\n\n"

    # write output to file
    with open(output_file, "w") as test:
        with open("maple2latex/out/primer") as primer:
            test.write(primer.read() + result + "\n\\end{document}\n")

if __name__ == '__main__':
    translate_files("maple2latex/functions", "maple2latex/out/test.tex")
