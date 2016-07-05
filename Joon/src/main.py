#!/usr/bin/env python
import os
from math_wrappers import MapleFile

translate = dict(tuple(line.split(" : ")) for line in open("keys/section_names").read().split("\n")
                 if line != "" and "%" not in line)

files = ["bessel", "modbessel", "confluent", "confluentlimit", "kummer", "parabolic",
         "whittaker", "apery", "archimedes", "catalan", "delian", "eulersconstant", "eulersnumber",
         "goldenratio", "gompertz", "naturallogarithm", "powerandroot", "pythagoras",
         "rabbit", "theodorus", "zeta2", "zeta4", "arccos", "arccosh", "arcsin", "arcsinh", "arctan", "arctanh",
         "cos", "cosh", "coth", "exp", "ln", "pow", "sin", "sinh", "tan", "tanh",
         "comperror", "error", "fresnel", "repint", "expintegrals", "related", "binet", "incompletegamma",
         "polygamma", "tetragamma", "trigamma"]

root_directory = "functions"

def main():
    """
    Generates and writes the results of traversing the root directory and translating all Maple files
    """
    root_depth = len(root_directory.split("/"))
    dirs = [d for d in os.walk(root_directory) if len(d[0].split("/")) == root_depth + 1]

    text = ""
    for info in dirs:
        depth = len(["" for ch in info[0] if ch == "/"])

        if depth == root_depth:  # section
            text += "\n\\section{" + translate[info[0].split("/")[-1]] + "}\n"

            for file_name in info[2]:
                folder = ''.join(file_name.split(".")[:-1])
                if folder in files:
                    text += "\\subsection{" + translate[folder] + "}\n" + \
                            MapleFile(info[0] + "/" + file_name).convert_formulae() + "\n\n"

    with open("output/test.tex", "w") as f:
        text = open("output/primer").read() + text + "\n\\end{document}"
        f.write(text)

    print "Successfully generated files in subsections: " + ', '.join(files)

if __name__ == '__main__':
    main()
