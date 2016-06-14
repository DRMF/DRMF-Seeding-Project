#!/usr/bin/env python

from TranslationMethods import parse_brackets
from TranslationMethods import make_frac
from TranslationMethods import replace_strings
from TranslationMethods import translate

SPECIAL = [['+\\left(-', '-\\left('], ['+\\frac{-', '-\\frac{'], ['+-', '-'], ['--', '+']]

class MapleFormula(object):
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

                elif line[0] in ["booklabel", "parameters", "general",
                                 "label", "constraints", "begin"]:
                    line[1] = line[1][1:-2].strip()

                elif line[0] in ["function", "lhs", "factor", "front",
                                 "even", "odd"]:
                    line[1] = line[1][:-1].strip()

                self.fields[line[0]] = line[1]

        # assign the information fields (about the equation)
        self.eq_type = self.fields["type"]
        self.category = self.fields["category"]
        self.label = self.fields["booklabel"]
        self.lhs = translate(self.fields["lhs"])

        if "general" in self.fields:
            self.general = [self.fields["general"]]

        elif "even" in self.fields and "odd" in self.fields:
            self.general = [self.fields["even"], self.fields["odd"]]

        if "factor" in self.fields:
            self.factor = translate(self.fields["factor"])

        if "front" in self.fields:
            self.front = translate(self.fields["front"])

        if "begin" in self.fields:
            self.begin = self.fields["begin"]

        self.modify_fields()

    def modify_fields(self):
        if self.eq_type == "series":
            self.general = translate(self.general[0])

        elif self.eq_type == "contfrac":
            self.general = parse_brackets(self.general[0]) # add handling later for even and odd

            if isinstance(self.general[0], list):
                self.general = self.general[0]

            if "begin" in self.fields:
                self.begin = parse_brackets(self.begin)

    def translate_to_latex(self):
        equation = "\\begin{equation*}\\tag{" + self.label + "}\n  " + self.lhs + "\n  = "

        # translates the Maple information (with spacing)
        if self.eq_type == "series":
            if "factor" in self.fields:
                equation += self.factor + " "
            equation += "\\sum_{k=0}^\\infty "

            if self.category == "power series":
                equation += self.general
            elif self.category == "asymptotic series":  # make sure to fix asymptotic series
                equation += "\\left(" + self.general + "\\right)"

        elif self.eq_type == "contfrac":
            start = 1  # in case the value of start isn't assigned

            if "begin" in self.fields:
                for piece in self.begin:
                    equation += make_frac(piece[0], piece[1]) + "+"
                    start += 1

            elif "front" in self.fields:
                equation += self.front + "+"
                start = 1

            if "factor" in self.fields:
                if self.factor == "-1":
                    equation += "-"
                else:
                    equation += self.factor + " "

            equation += "\\CFK{m}{" + str(start) + "}{\\infty}@{" + self.general[0] + "}{" + self.general[1] + "}"

        # adds metadata
        # equation += "\n  %  \\constraint{$" + self.constraints + "$}"
        equation += "\n  %  \\category{" + self.category + "}"
        equation += "\n\\end{equation*}"

        return replace_strings(equation, SPECIAL)

    def __str__(self):
        text = ""

        for s in self.fields:
            text += s + ": " + self.fields[s] + "\n"

        return text
