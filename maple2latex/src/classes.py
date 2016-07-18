#!/user/bin/env python

from translation_methods import make_equation
from copy import copy


class MapleFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.formulae = self.obtain_formulae()

    def obtain_formulae(self):
        contents = open(self.filename).read()

        return [MapleEquation(piece.split("\n")) for piece in contents.split("create(")
                if "):" in piece or ");" in piece]

    def convert_formulae(self):
        return '\n\n'.join([make_equation(copy(formula)) for formula in self.formulae])

    def __str__(self):
        return "MapleFile of " + self.filename


class MapleEquation(object):
    def __init__(self, inp):
        # creates a dictionary called "fields", containing all the Maple fields
        self.fields = {"category": "", "constraints": "", "begin": "", "factor": "", "front": "", "parameters": "",
                       "type": inp.pop(0).split("'")[1]}

        for i, line in enumerate(inp):
            line = line.split(" = ", 1)

            if len(line) > 1:
                line[0] = line[0].strip()

                if line[0] in ["category"]:
                    line[1] = line[1].strip()[1:-1].strip()

                elif line[0] == "begin" and "proc (x) [1, x] end proc" in line[1]:
                    temp = [[1, int(d)] for d in inp[i + 2].split(",")]
                    if len(temp) > 10:
                        temp = temp[:10]
                    line[1] = str(temp)[1:-1]

                elif line[0] == "booklabelv1" and line[1] == '"",':
                    line[1] = "No label"

                elif line[0] in ["booklabelv1", "booklabelv2", "general", "constraints", "begin", "parameters"]:
                    line[1] = line[1].strip()[1:-2].strip()

                elif line[0] in ["lhs", "factor", "front", "even", "odd"]:
                    if line[1].strip()[-1] == ",":
                        line[1] = line[1].strip()[:-1]
                    line[1] = line[1].strip()
                self.fields[line[0]] = line[1]

        # assign fields containing information about the equation
        self.eq_type = self.fields["type"]
        self.category = self.fields["category"]
        self.label = self.fields["booklabelv1"]
        self.lhs = self.fields["lhs"]
        self.factor = self.fields["factor"]
        self.front = self.fields["front"]
        self.begin = self.fields["begin"]
        self.constraints = self.fields["constraints"]
        self.parameters = self.fields["parameters"]

        # even-odd case handling
        if "general" in self.fields:
            self.general = [self.fields["general"]]
        elif "even" in self.fields and "odd" in self.fields:
            self.general = [self.fields["even"], self.fields["odd"]]

    def __str__(self):
        return '\n'.join([s + ": " + self.fields[s] for s in self.fields])
