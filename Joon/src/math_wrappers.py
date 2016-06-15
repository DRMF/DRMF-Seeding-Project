#!/user/bin/env python

from translation_methods import make_equation
from copy import copy

class MapleFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.formulae = self.obtain_formulae()

    def obtain_formulae(self):
        contents = open(self.filename).read()

        return [MapleEquation(piece) for piece in contents.split("create(") if "):" in piece or ");" in piece]

    def convert_formulae(self):
        return '\n\n'.join([make_equation(copy(formula)) for formula in self.formulae])

    def __str__(self):
        return "MapleFile of " + self.filename

class MapleEquation(object):
    def __init__(self, inp):
        inp = inp.split("\n")

        # creates a dictionary called "fields", containing all the Maple fields
        self.fields = dict()
        for i, line in enumerate(inp):
            if i == 0:
                self.fields["type"] = line.split("'")[1]

            elif " = " in line:
                line = line.split(" = ")
                line[0] = line[0].strip()

                if line[0] in ["category"]:
                    line[1] = line[1][1:-1].strip()

                elif line[0] in ["booklabel", "general", "constraints", "begin"]:
                    line[1] = line[1][1:-2].strip()

                elif line[0] in ["lhs", "factor", "front", "even", "odd"]:
                    line[1] = line[1][:-1].strip()

                self.fields[line[0]] = line[1]

        # assign the information fields (about the equation)
        self.eq_type = self.fields["type"]
        self.category = self.fields["category"]
        self.label = self.fields["booklabel"]
        self.lhs = self.fields["lhs"]

        if "general" in self.fields:
            self.general = [self.fields["general"]]

        elif "even" in self.fields and "odd" in self.fields:
            self.general = [self.fields["even"], self.fields["odd"]]

        if "factor" in self.fields:
            self.factor = self.fields["factor"]

        if "front" in self.fields:
            self.front = self.fields["front"]

        if "begin" in self.fields:
            self.begin = self.fields["begin"]

    def __str__(self):
        return [s + ": " + self.fields[s] + "\n" for s in self.fields]
