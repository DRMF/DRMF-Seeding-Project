#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

import copy
import json
import sys
from string import ascii_lowercase
from maple_tokenize import tokenize

INFO = json.loads(open("maple2latex/data/keys.json").read())

FUNCTIONS = INFO["functions"]
SYMBOLS = INFO["symbols"]
CONSTRAINTS = INFO["constraints"]

SPECIAL = {"(": "\\left(", ")": "\\right)", "+-": "-", "\\subplus-": "-", "^{1}": "", "\\inNot": "\\notin"}

MULTI_ARGS = ["sin", "cos", "tan", "arccos", "arccosh", "arcsin", "arcsinh", "arctanh", "sinh", "cosh", "coth", "tanh",
              "erfc", "erf", "log", "ln"]


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
            self.general = self.fields["general"]
        elif "even" in self.fields and "odd" in self.fields:
            self.general = [self.fields["even"], self.fields["odd"]]


class LatexEquation(object):
    def __init__(self, label, equation, metadata):
        self.label = label
        self.equation = equation
        self.metadata = metadata

    @classmethod
    def from_maple(cls, eq):
        # (List[MapleEquation]) -> LatexEquation
        # modify fields
        eq.lhs = translate(eq.lhs)
        eq.factor = translate(eq.fields["factor"])
        eq.front = translate(eq.fields["front"])
        eq.begin = parse_brackets(eq.begin)

        if eq.factor == "1":
            eq.factor = ""

        equation = eq.lhs + "\n  = "
        metadata = dict()

        # translates the Maple information (with spacing)
        if eq.eq_type == "series":
            # add factor and front with accompanying symbols, if they exist
            equation += evaluate(eq.factor + " ", eq.factor) + evaluate(eq.front + "+", eq.front)
            equation += "\\sum_{k=0}^\\infty "

            eq.general = translate(eq.general)

            if eq.category == "power series":
                equation += eq.general
            elif eq.category == "asymptotic series":  # make sure to fix asymptotic series
                equation += "(" + eq.general + ")"

        elif eq.eq_type == "contfrac":
            # obtain data from eq.general
            try:
                pieces = parse_brackets(eq.general)
            except AttributeError:  # in form of even, odd
                pieces = list()
                for piece in eq.general:
                    pieces += parse_brackets(piece)

            # if there are multiple forms (requires substitution)
            if len(pieces) > 1:
                metadata["substitution"] = ','.join(perform_substitution(eq, pieces))
                pieces = ["s_m", "1"]
            else:
                pieces = pieces[0]

            start = 1  # in case the value of start isn't assigned

            # add terms before general
            equation += evaluate(eq.front + "+", eq.front)

            for piece in eq.begin:
                equation += make_frac(piece) + " \\subplus "
                start += 1

            if eq.factor == "-1":
                equation += "-"
            else:
                equation += evaluate(eq.factor + " ", eq.factor)

            # trim unnecessary parentheses
            for i, element in enumerate(pieces):
                pieces[i] = trim_parens(translate(element))

            if pieces != ["0", "1"]:
                equation += "\\CFK{m}{" + str(start) + "}{\\infty}@@{" + pieces[0] + "}{" + pieces[1] + "}"
            else:
                equation += "\\dots"

        metadata["constraint"] = translate(eq.constraints)
        metadata["category"] = eq.category
        metadata["mapletag"] = eq.label

        return cls(eq.label, replace_strings(equation, SPECIAL), metadata)

    @staticmethod
    def get_sortable_label(equation):
        if equation.label == "":
            return [sys.maxsize, sys.maxsize, sys.maxsize]

        label = copy.copy(equation.label)
        for i, ch in enumerate(ascii_lowercase):
            if label[-1] == ch:
                label = label[:-1] + "." + str(i + 1)

        return map(int, filter(lambda x: x != "", label.split(".")))

    def __str__(self):
        metadata = ""
        for data_type, data in self.metadata.iteritems():
            if data == "":
                continue

            if data_type in ["constraint", "substitution"]:  # mathmode
                metadata += "  %  \\" + data_type + "{$" + replace_strings(data, SPECIAL) + "$}\n"
            else:
                metadata += "  %  \\" + data_type + "{" + data + "}\n"\

        return "\\begin{equation}\n  " + self.equation + "\n" + metadata + "\\end{equation}\n"


def evaluate(data, key):
    # (Any, bool) -> Any
    """
    Will return data as long as key is not False.
    If key is False, returns 0 or blank string, depending on type(data).
    Used as replacement for "if data != "": ...", and similar statements.
    """
    return data * bool(key)


def replace_strings(string, keys):
    # type: (str, dict) -> str
    """Replaces key strings with their mapped value."""
    for key in list(keys):
        string = string.replace(key, keys[key])

    return string


def parse_brackets(string):
    # type: (str) -> List[str]
    """Obtains the contents from data encapsulated in square brackets."""

    if not string:
        return ""

    exp = string[1:-1].split(",")
    for i, e in enumerate(exp):
        exp[i] = replace_strings(e, {"[": "", "]": ""}).strip()

    i = 0
    while i + 1 < len(exp):
        exp[i] = [exp[i], exp.pop(i+1)]
        i += 1

    return exp


def trim_parens(exp):
    # type: (str/List[str]) -> str
    """Removes unnecessary parentheses."""

    if type(exp) in [unicode, str] and exp == "":
        return ""
    elif type(exp) == list and exp == []:
        return []

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

        return test

    return exp


def make_frac(parts):
    # type: (List[str]) -> str
    """Generate a LaTeX fraction from its numerator and denominator."""

    return translate("(" + parts[0] + ") / (" + parts[1] + ")")


def basic_translate(exp):
    # type: (List[str]) -> str
    """Translates basic mathematical operations."""

    # translates operations in place
    for order in range(3):  # order of operations
        i = 0
        while i < len(exp):
            modified = False

            # factorial
            if exp[i] == "!" and order == 0:
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


def perform_substitution(eq, forms):
    # (MapleEquation, List[str]) -> List[str]
    """Performs variable substitutions on the strings in eq.general."""

    replacements = list()
    if len(eq.general) == 2:
        replacements = ["2j", "2j+1"]
    elif forms:
        for i, _ in enumerate(forms):
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

    return forms


def get_arguments(function_name, arg_string):
    # type: (str, List[str]) -> (List[str], List[str])
    """Generates the function pieces and the arguments."""

    parens_mod = False

    # no arguments
    if not arg_string:  # arg_string == []
        args = []

    # handling for not
    elif function_name == "not":
        inversion = {"<": "\\geq ", ">": "\\leq ", "\\in": "\\notin "}

        for i, ch in enumerate(arg_string):
            if ch in inversion:
                arg_string[i] = inversion[ch]

        args = [basic_translate(arg_string)]

    # handling for ranges (constraints)
    elif function_name == "RealRange":
        for i, piece in enumerate(arg_string):
            if trim_parens(piece) != piece:
                arg_string[i] = trim_parens(piece)

        args = basic_translate(arg_string).split(",")

    # handling for trigamma
    elif function_name == "Psi" and arg_string[0] == "1":
        function_name = "special-trigamma"
        args = [basic_translate(arg_string[2])]

    # handling for hypergeometric, q-hypergeometric functions
    elif function_name in ["hypergeom", "qhyper"]:
        args = list()
        for s in ' '.join(arg_string).split("] , "):
            args.append(basic_translate(replace_strings(s, {"[": "", "]": ""}).split()))

        if function_name == "qhyper":
            args += args.pop(2).split(",")

        for p, i in enumerate([1, 0]):
            arg_count = evaluate(args[i + p].count(",") + 1, args[i + p])
            args.insert(0, str(arg_count))

    # handling for sums
    elif function_name == "sum":
        args = basic_translate(arg_string).split(",")
        args = args.pop(1).split("..") + [args[0]]
        if args[1] == "infinity":
            args[1] = "\\infty"

    # handling for function in case it has optional parentheses
    elif function_name in MULTI_ARGS and len(arg_string) == 1:
        parens_mod = True
        args = basic_translate(arg_string).split(",")

    else:
        args = basic_translate(arg_string).split(",")

    result = list()
    for function in FUNCTIONS:
        for variant in FUNCTIONS[function]:
            if function_name == function and len(args) == variant["args"]:
                result = copy.copy(variant["repr"])

    # modify macro to form without parentheses
    if parens_mod:
        result[0] = result[0].replace("@", "@@")

    return [result, args]


def generate_function(name, args):
    # type: (str, List[str]) -> str
    """Generate a function with the provided function name and arguments."""

    result, args = get_arguments(name, args)

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
                piece = generate_function(exp[i], trim_parens(piece))

            else:
                piece = basic_translate(piece)

            # remove unnecessary parentheses around fractions
            if "frac" in replace_strings(piece, {"(": ""})[:6] and (r + 2 > len(exp) or exp[r + 1] != "^"):
                while piece != trim_parens(piece):
                    piece = trim_parens(piece)

            exp = exp[0:i] + [piece] + exp[r + 1:]

        i -= 1

    return basic_translate(exp)
