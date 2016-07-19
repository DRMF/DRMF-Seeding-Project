#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

import copy
import json
from src.maple_tokenize import tokenize

INFO = json.loads(open("data/keys.json").read())

FUNCTIONS = INFO["functions"]
SYMBOLS = INFO["symbols"]
CONSTRAINTS = INFO["constraints"]

SPECIAL = {"(": "\\left(", ")": "\\right)", "+-": "-", "\\subplus-": "-", "^{1}": "", "\\inNot": "\\notin"}


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


def replace_strings(string, keys):
    # type: (str, dict) -> str
    """Replaces key strings with their mapped value."""
    for key in list(keys):
        string = string.replace(key, keys[key])

    return string


def parse_brackets(exp):
    # type: ((str, list)) -> list
    """Obtains the contents from data encapsulated in square brackets."""

    exp = exp[1:-1].split(",")
    for i, e in enumerate(exp):
        exp[i] = replace_strings(e, {"[": "", "]": ""}).strip()

    i = 0
    while i + 1 < len(exp):
        exp[i] = [exp[i], exp.pop(i+1)]
        i += 1

    return exp


def trim_parens(exp):
    # type: (str) -> str
    """Removes unnecessary parentheses."""

    if exp == "":
        return ""

    # checks whether the outer set of parentheses are necessary
    if exp[0] == "(" and exp[-1] == ")":
        test = exp[1:-1]

        # validate whether test is correct (in terms of parentheses)
        s = list()  # stack
        for ch in test:
            if ch == "(":
                s.append(ch)
            elif ch == ")":
                if len(s) == 0:
                    return exp
                else:
                    s.pop()

        if len(s) != 0:
            return exp

        return test

    return exp


def make_frac(parts):
    # type: (list) -> str
    """Generate a LaTeX fraction from its numerator and denominator."""

    return translate("(" + parts[0] + ") / (" + parts[1] + ")")


def basic_translate(exp):
    # type: (list) -> str
    """Translates basic mathematical operations."""

    for order in range(3):
        i = 0
        while i < len(exp):
            modified = False

            if exp[i] == "I":
                exp[i] = "i"

            elif exp[i] == "!" and order == 0:
                exp[i - 1] += "!"
                modified = True

            elif exp[i] == "^" and order == 0:
                power = trim_parens(exp.pop(i + 1))
                exp[i - 1] += "^{" + power + "}"
                modified = True

            elif exp[i] == "*" and order == 1:
                if exp[i - 1][-1] not in "}]" and "\\" in exp[i - 1] and exp[i + 1][0] != "\\":
                    exp[i - 1] += " "

                exp[i - 1] += exp.pop(i + 1)
                modified = True

            elif exp[i] == "/" and order == 1:
                for index in [i - 1, i + 1]:
                    exp[index] = trim_parens(exp[index])
                exp[i - 1] = "\\frac{" + exp[i - 1] + "}{" + exp.pop(i + 1) + "}"
                modified = True

            if modified:
                exp.pop(i)
                i -= 1
            else:
                i += 1

    return ''.join(exp)


def get_arguments(function, arg_string):
    # type: (str, list) -> list
    """Obtains the arguments of a function."""

    if arg_string == ["(", ")"]:
        return []

    elif function in ["hypergeom", "qhyper"]:
        args = list()
        for s in ' '.join(arg_string[1:-1]).split("] , "):
            args.append(basic_translate(replace_strings(s, {"[": "", "]": ""}).split()))

        if function == "qhyper":
            args += args.pop(2).split(",")

        for p, i in enumerate([1, 0]):
            arg_count = 0
            if args[i + p] != "":
                arg_count = args[i + p].count(",") + 1

            args.insert(0, str(arg_count))

    elif function == "sum":
        args = basic_translate(arg_string[1:-1]).split(",")
        args = args.pop(1).split("..") + [args[0]]
        if args[1] == "infinity":
            args[1] = "\\infty"

    else:
        args = basic_translate(arg_string[1:-1]).split(",")

    return args


def generate_function(name, args):
    # type: (str, list) -> str
    """Generate a function with the provided function name and arguments."""

    result = list()
    for n in FUNCTIONS:
        for variant in FUNCTIONS[n]:
            if name == n and len(args) == variant["args"]:
                result = copy.copy(variant["repr"])

    for n in range(1, len(result)):
        result.insert(2 * n - 1, args[n - 1])

    return ''.join(result)


def translate(exp):
    # type: (str) -> str
    """Format Maple code as LaTeX."""

    if exp == "":
        return ""

    exp = replace_strings(exp.strip(), CONSTRAINTS)
    exp = replace_strings(exp, {"functions:-": ""})
    exp = tokenize(exp)

    for i in range(len(exp)):
        if exp[i] in SYMBOLS:
            exp[i] = SYMBOLS[exp[i]]

    i = len(exp) - 1
    while i >= 0:
        if exp[i] == "(":
            r = i + exp[i:].index(")")
            piece = exp[i:r + 1]

            if exp[i - 1] == "]":
                sq = i - 2 - exp[:i - 1][::-1].index("[")
                piece = [piece[0]] + exp[sq + 1:i - 1] + [","] + piece[1:]
                i = sq

            if exp[i - 1] in FUNCTIONS:
                i -= 1
                piece = generate_function(exp[i], get_arguments(exp[i], piece))

            else:
                piece = basic_translate(piece)

            if "frac" in replace_strings(piece, {"(": ""})[:6] and (r + 2 > len(exp) or exp[r + 1] != "^"):
                while piece != trim_parens(piece):
                    piece = trim_parens(piece)

            exp = exp[0:i] + [piece] + exp[r + 1:]

        i -= 1

    return basic_translate(exp)


def make_equation(eq, view_metadata=False):
    # type: (MapleEquation{, bool}) -> str
    """Make a LaTeX equation based on a MapleEquation object."""

    eq.lhs = translate(eq.lhs)
    eq.factor = translate(eq.fields["factor"])
    eq.front = translate(eq.fields["front"])

    if eq.eq_type == "series":
        eq.general = translate(eq.general[0])

    elif eq.eq_type == "contfrac":
        eq.general = parse_brackets(eq.general[0])[0]

        if eq.begin != "":
            eq.begin = parse_brackets(eq.begin)

    equation = "\\begin{equation*}\\tag{" + eq.label + "}\n  " + eq.lhs + "\n  = "

    if eq.factor == "1":
        eq.factor = ""

    # translates the Maple information (with spacing)
    if eq.eq_type == "series":
        if eq.factor != "":
            equation += eq.factor + " "

        elif eq.front != "":
            equation += eq.front + "+"

        equation += "\\sum_{k=0}^\\infty "

        if eq.category == "power series":
            equation += eq.general
        elif eq.category == "asymptotic series":  # make sure to fix asymptotic series
            equation += "(" + eq.general + ")"

    elif eq.eq_type == "contfrac":
        start = 1  # in case the value of start isn't assigned

        if eq.front != "":
            equation += eq.front + "+"
            start = 1

        if eq.begin != "":
            for piece in eq.begin:
                equation += make_frac(piece) + " \\subplus "
                start += 1

        if eq.factor != "":
            if eq.factor == "-1":
                equation += "-"
            else:
                equation += eq.factor + " "

        for i, element in enumerate(eq.general):
            eq.general[i] = trim_parens(translate(element))

        if eq.general != ["0", "1"]:
            equation += "\\CFK{m}{" + str(start) + "}{\\infty}@@{" + eq.general[0] + "}{" + eq.general[1] + "}"
        else:
            equation += "\\dots"

    # adds metadata
    if view_metadata:
        equation += "\n\\end{equation*}"
        equation += "\n\\begin{center}"
        equation += "\nParameters: $$" + eq.parameters + "$$"
        equation += "\n$$" + translate(eq.constraints) + "$$"
        equation += "\n" + eq.category
        equation += "\n\\end{center}"
    else:
        equation += "\n  %  \\constraint{$" + translate(eq.constraints) + "$}"
        equation += "\n  %  \\category{" + eq.category + "}"
        equation += "\n\\end{equation*}"

    return replace_strings(equation, SPECIAL)
