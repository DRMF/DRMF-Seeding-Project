#!/usr/bin/env python
import os
from objects import MapleFile
from translation_methods import sort

translate = dict(tuple(line.split(" : ")) for line in open("info/section_names").read().split("\n")
                 if line != "" and "%" not in line)

files = [
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

root_directory = "functions"

def translate_file(filename):
    """
    Translates all the formulae in a file
    """

    with open("output/test.tex", "w") as f:
        f.write(open("output/primer").read() + MapleFile(filename).convert_formulae() + "\n\\end{document}")

    print "Successfully translated formulae in " + filename

def translate_directories():
    """
    Generates and writes the results of traversing the root directory and translating all Maple files
    """

    root_depth = len(root_directory.split("/"))
    dirs = [d for d in os.walk(root_directory) if len(d[0].split("/")) == root_depth + 1]

    master_tags = dict()

    result = ""
    for info in dirs:
        depth = len(["" for ch in info[0] if ch == "/"])

        if depth == root_depth:  # section
            file_info = dict()
            text = "\n\\section{" + translate[info[0].split("/")[-1]] + "}\n"

            for file_name in info[2]:
                folder = ''.join(file_name.split(".")[:-1])
                if folder in files:
                    t = MapleFile(info[0] + "/" + file_name).convert_formulae()
                    eq_number = filter(str.isdigit, str(t.split("\n")[0])).rjust(20)
                    file_info[eq_number] = [folder, t]

            tags = list(file_info)
            tags.sort()

            for tag in tags:
                text += "\\subsection{" + translate[file_info[tag][0]] + "}\n" + file_info[tag][1] + "\n\n"

            if len(tags) > 0:
                master_tags[tags[0]] = text

    tags = list(master_tags)
    tags.sort()

    for tag in tags:
        result += "\n" + master_tags[tag]

    with open("output/test.tex", "w") as f:
        result = open("output/primer").read() + result + "\n\\end{document}"
        f.write(result)

    print "Success"

if __name__ == '__main__':
    translate_directories()
