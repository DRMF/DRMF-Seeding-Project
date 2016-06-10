#!/usr/bin/env python

from MapleFormula import MapleFormula

class MapleFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.formulae = self.obtain_formulae()

    def obtain_formulae(self):
        contents = open(self.filename).read()

        return [MapleFormula(piece) for piece in contents.split("create(") if "):" in piece]

    def convert_formulae(self):
        text = ""
        for formula in self.formulae:
            text += formula.translate_to_latex() + "\n\n"

        return text

def main():
    files = ["functions/BS/bessel/bessel.mpl", "functions/BS/modbessel/modbessel.mpl",
             "functions/CH/confluent/confluent.mpl", "functions/CH/confluent/confluent.mpl"]

    text = ""

    for file_name in files:
        m_file = MapleFile(file_name)
        text += "Output for " + file_name + "\n"
        text += m_file.convert_formulae()
        text += "\n\n\n"

        print "Output for " + file_name + "\n"
        print m_file.convert_formulae()

    with open("output/test.tex", "w") as f:
        text = open("output/primer").read() + text + "\\end{document}"
        f.write(text)

if __name__ == "__main__":
    main()