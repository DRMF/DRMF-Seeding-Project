#!/usr/bin/env python
import os
from classes import MapleFile

TABLE = dict()
with open("info/section_names") as name_info:
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
    "qhyper"
]

ROOT = "functions"


def translate_file(filename: str):
    """Translates all the formulae in a file."""

    with open("out/test.tex", "w") as test, open("out/primer") as primer:
        test.write(primer.read() + MapleFile(filename).convert_formulae() + "\n\\end{document}")


def translate_directories():
    """Generates and writes the results of traversing the root directory and translating all Maple files."""

    root_depth = len(ROOT.split("/"))

    dirs = [d for d in os.walk(ROOT) if d[0].count("/") == root_depth]

    result = ""

    for info in dirs:
        depth = len(["" for ch in info[0] if ch == "/"])

        if depth == root_depth:  # section
            result += "\n\\section{" + TABLE[info[0].split("/")[-1]] + "}\n"

            for file_name in info[2]:
                folder = ''.join(file_name.split(".")[:-1])
                if folder in FILES:
                    result += "\\subsection{" + TABLE[folder] + "}\n" + \
                              MapleFile(info[0] + "/" + file_name).convert_formulae() + "\n\n"

    with open("out/test.tex", "w") as test, open("out/primer") as primer:
        test.write(primer.read() + result + "\n\\end{document}")

if __name__ == '__main__':
    translate_directories()
