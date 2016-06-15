#!/usr/bin/env python

from math_wrappers import MapleFile
from category_generator import translate as section_headers

def main():
    files = ["functions/BS/bessel/bessel.mpl", "functions/BS/modbessel/modbessel.mpl",
             "functions/CH/confluent/confluent.mpl", "functions/CH/confluent/confluent.mpl",
             "functions/CH/confluentlimit/confluentlimit.mpl", "functions/CH/kummer/kummer.mpl",
             "functions/CH/parabolic/parabolic.mpl", "functions/CH/whittaker/whittaker.mpl",
             "functions/CN/apery/apery.mpl"]

    text = ""

    for file_name in files:
        m_file = MapleFile(file_name)
        file_name = file_name.split("/")[-2]
        section_name = section_headers[file_name]
        text += "\\section{" + section_name + "}\n\n"
        text += m_file.convert_formulae()
        text += "\n\n"

    print text

    with open("output/test.tex", "w") as f:
        text = open("output/primer").read() + text + "\\end{document}"
        f.write(text)

if __name__ == "__main__":
    main()