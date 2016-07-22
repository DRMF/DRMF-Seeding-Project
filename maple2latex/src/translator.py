#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

import copy
import json
from string import ascii_lowercase
from maple_tokenize import tokenize

INFO = json.loads(open("maple2latex/data/keys.json").read())

FUNCTIONS = INFO["functions"]
SYMBOLS = INFO["symbols"]
CONSTRAINTS = INFO["constraints"]

SPECIAL = {"(": "\\left(", ")": "\\right)", "+-": "-", "\\subplus-": "-", "^{1}": "", "\\inNot": "\\notin",
           "\\ImaginaryNumber": "i"}

# TODO: gamma_chisquare.mpl (no macro.)
# TODO: normal.mpl (no macro.)


class MapleEquation(object):
    def __init__(self, inp):
        # creates a dictionary called "fields", containing all the Maple fields
        self.fields = {"category": "", "constraints": "", "begin": "", "factor": "", "front": "", "parameters": "",
                       "type": inp.pop(0).split("'")[1]}

        # read data from the Maple create() statement
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
                    line[1] = "x.x.x"

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


class LatexEquation(object):
    def __init__(self, label, equation, metadata):
        self.label = label
        self.equation = equation
        self.metadata = metadata

    @classmethod
    def from_maple(cls, eq):
        # modify fields
        eq.lhs = translate(eq.lhs)
        eq.factor = translate(eq.fields["factor"])
        eq.front = translate(eq.fields["front"])

        equation = eq.lhs + "\n  = "

        if eq.factor == "1":
            eq.factor = ""

        metadata = dict()

        # translates the Maple information (with spacing)
        if eq.eq_type == "series":
            eq.general = translate(eq.general[0])

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
            forms = list()

            if len(parse_brackets(eq.general[0])) > 1:
                # print eq.label
                forms = parse_brackets(eq.general[0])

            if len(eq.general) == 2 or forms:
                if not forms:  # forms is empty
                    for form in eq.general:
                        forms += parse_brackets(form)

                replacements = list()
                if len(eq.general) == 2:
                    replacements = ["2j", "2j+1"]
                elif forms:
                    for i in range(len(forms)):
                        replacement = str(len(forms)) + "j"
                        if i < len(forms) - 1:
                            replacement += "-" + str(len(forms) - i - 1)

                        replacements.append(replacement)

                for i, form in enumerate(forms):
                    for j, half in enumerate(form):
                        half = tokenize(half)
                        for k, ch in enumerate(half):
                            if ch == "m":
                                half[k] = "(" + replacements[i] + ")"

                        form[j] = ' '.join(half)

                    forms[i] = "s_{" + replacements[i] + "} = " + make_frac(form)

                metadata["substitution"] = ','.join(forms)
                pieces = ["s_m", "1"]

            else:
                pieces = parse_brackets(eq.general[0])[0]

            if eq.begin != "":
                eq.begin = parse_brackets(eq.begin)

            start = 1  # in case the value of start isn't assigned

            # add terms before general
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

            # trim unnecessary parentheses
            for i, element in enumerate(pieces):
                pieces[i] = trim_parens(translate(element))

            if pieces != ["0", "1"]:
                equation += "\\CFK{m}{" + str(start) + "}{\\infty}@@{" + pieces[0] + "}{" + pieces[1] + "}"
            else:
                equation += "\\dots"

        metadata["constraint"] = translate(eq.constraints)
        metadata["category"] = eq.category

        return cls(eq.label, replace_strings(equation, SPECIAL), metadata)

    @classmethod
    def get_sortable_label(cls, equation):
        if equation.label == "x.x.x":
            return [100, 100, 100]  # should be three very large numbers

        label = copy.copy(equation.label)
        for i, ch in enumerate(ascii_lowercase):
            if label[-1] == ch:
                label = label[:-1] + "." + str(i + 1)

        if label[-1] == ".":
            label = label[:-1]

        return map(int, label.split("."))

    def __str__(self):
        metadata = ""
        for data_type, data in self.metadata.iteritems():
            if data_type in ["constraint", "substitution"]:  # mathmode
                metadata += "  %  \\" + data_type + "{" + replace_strings(data, SPECIAL) + "}\n"
            else:
                metadata += "  %  \\" + data_type + "{" + data + "}\n"

            # if data_type in ["substitution"]:
            #     metadata += "  " + replace_strings(data, SPECIAL) + "\n"

        return "\\begin{equation*}\\tag{" + self.label + "}\n  " + self.equation + "\n" + \
               metadata + "\\end{equation*}\n"


def replace_strings(string, keys):
    # type: (str, dict) -> str
    """Replaces key strings with their mapped value."""
    for key in list(keys):
        string = string.replace(key, keys[key])

    return string


def parse_brackets(string):
    # type: ((str, list)) -> list
    """Obtains the contents from data encapsulated in square brackets."""

    exp = string[1:-1].split(",")
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

    # translates operations in place
    for order in range(3):  # order of operations
        i = 0
        while i < len(exp):
            modified = False

            # the imaginary number
            if exp[i] == "I":
                exp[i] = "\\ImaginaryNumber"

            # factorial
            elif exp[i] == "!" and order == 0:
                exp[i - 1] += "!"
                modified = True

            # power
            elif exp[i] == "^" and order == 0:
                power = trim_parens(exp.pop(i + 1))
                exp[i - 1] += "^{" + power + "}"
                modified = True

            # multiplication
            elif exp[i] == "*" and order == 1:
                # adds spacing when necessary
                if exp[i - 1][-1] not in "}]" and "\\" in exp[i - 1] and exp[i + 1][0] != "\\":
                    exp[i - 1] += " "

                exp[i - 1] += exp.pop(i + 1)
                modified = True

            # division
            elif exp[i] == "/" and order == 1:
                # remove extra parentheses
                for index in [i - 1, i + 1]:
                    exp[index] = trim_parens(exp[index])
                exp[i - 1] = "\\frac{" + exp[i - 1] + "}{" + exp.pop(i + 1) + "}"
                modified = True

            # removes extra characters
            if modified:
                exp.pop(i)
                i -= 1
            else:
                i += 1

    return ''.join(exp)


def get_arguments(function, arg_string):
    # type: (str, list) -> list
    """Obtains the arguments of a function."""

    # no arguments
    if arg_string == ["(", ")"]:
        return []

    # handling for hypergeometric, q-hypergeometric functions
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

    # handling for sums
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

    # places arguments between shell of function
    for n in range(1, len(result)):
        result.insert(2 * n - 1, args[n - 1])

    return ''.join(result)


def translate(exp):
    # type: (str) -> str
    """Format Maple code as LaTeX."""

    if exp == "":
        return ""

    # initial formatting of input string
    exp = replace_strings(exp.strip(), CONSTRAINTS)
    exp = replace_strings(exp, {"functions:-": ""})
    exp = tokenize(exp)

    for i, s in enumerate(exp):
        if exp[i] in SYMBOLS:
            exp[i] = SYMBOLS[s]

    i = len(exp) - 1
    while i >= 0:
        if exp[i] == "(":  # handle contents between parentheses
            r = i + exp[i:].index(")")
            piece = exp[i:r + 1]

            if exp[i - 1] == "]":  # for logarithm function
                sq = i - 2 - exp[:i - 1][::-1].index("[")
                piece = [piece[0]] + exp[sq + 1:i - 1] + [","] + piece[1:]
                i = sq

            if exp[i - 1] in FUNCTIONS:  # handling for functions
                i -= 1
                piece = generate_function(exp[i], get_arguments(exp[i], piece))

            else:
                piece = basic_translate(piece)

            # remove unnecessary parentheses around fractions
            if "frac" in replace_strings(piece, {"(": ""})[:6] and (r + 2 > len(exp) or exp[r + 1] != "^"):
                while piece != trim_parens(piece):
                    piece = trim_parens(piece)

            exp = exp[0:i] + [piece] + exp[r + 1:]

        i -= 1

    return basic_translate(exp)
