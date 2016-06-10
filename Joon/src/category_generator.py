#!/usr/bin/env python
import os

INDENT = "    "

names = ["BS", "CH", "CN", "EF", "ER", "EX", "GA", "HY", "QH", "SM"]

translate = dict(tuple(line.split(" : ")) for line in open("keys/section_names").read().split("\n")
                       if line != "" and "%" not in line)

print translate

def generate_categories():
    """
    Generates section, subsection
    """

    root_directory = "functions"
    depth = len(root_directory.split("/"))
    dirs = [d for d in os.walk(root_directory)]
    text = ""
    subsections = {"no-subsection": list()}

    for info in dirs:
        print info

        directory = info[0].split("/")

        if len(directory) == depth+1:
            if text:
                for subsection in subsections:
                    text += "    \\subsection{"+subsection+"}\n"
                    for file_name in subsections[subsection]:
                        text += "      "+file_name+"\n"
                    text += "\n"

            text += "  \\section{"+translate[directory[depth]]+"}\n"
            subsections = {"no-subsection": list()}

        elif len(directory) == depth+2 and translate[directory[depth+1]] not in subsections:
            if "no-subsection" in subsections:
                subsections.pop("no-subsection")

            subsections[translate[directory[depth+1]]] = list()

    print text

    with open("output/test.tex", "w") as f:
        text = open("output/primers/primer").read() + text + "\\end{document}"
        f.write(text)

def main():
    generate_categories()

if __name__ == '__main__':
    main()
