#!/usr/bin/env python

import sys

# Constants
functions = dict(tuple(line.split(" || ", 1)) for line in open("keys/functions").read().split("\n")
                 if line != "" and "%" not in line)
symbols = dict(tuple(line.split(" || ")) for line in open("keys/symbols").read().split("\n")
               if line != "" and "%" not in line)
spacing = list((char, " " + char + " ") for char in ["(", ")", "+", "-", "*", "/", "^", "<", ">", ",", "::"])
special = [["(", "\\left("], [")", "\\right)"], ["+-", "-"], ["\\subplus-", "-"], ["^{1}", ""]]
constraints = list(tuple(line.split(" || ")) for line in open("keys/constraints").read().split("\n")
                   if line != "" and "%" not in line)
numbers = "0123456789"

def replace_strings(string, li):
    """
    Replaces multiple strings with multiple other strings, stored in lists of length two in li.
    The first element is the string to find, and the second element is the replacement string.
    """

    for key in li:
        string = string.replace(key[0], key[1])

    return string

def parse_brackets(exp):
    """
    Translates the contents between a set of square brackets
    """

    if "],[" in exp[1:-1]:
        splitter = "],["
    else:
        splitter = "], ["

    return [[replace_strings(p, [["[", ""], ["]", ""]]) for p in piece.split(",")]
            for piece in exp[1:-1].split(splitter)]

def make_frac(parts):
    """
    Generate a LaTeX frac from its parts [numerator, denominator]
    """

    return translate("(" + parts[0] + ") / (" + parts[1] + ")")

def parse_arguments(pieces):
    if pieces == "()":
        return []

    pieces = pieces[1:-1].split(",")

    for i, piece in enumerate(pieces):
        if piece[0] == "[" and piece[-1] != "]":
            pieces[i] = (pieces[i] + "," + pieces.pop(i + 1))[1:-1]
        elif piece[0] == "[" and piece[-1] == "]":
            pieces[i] = pieces[i][1:-1]

    return pieces

def verify_validity(exp):
    """
    Verifies the validity of an expression in terms of parentheses grouping
    """

    left = list()

    try:
        for ch in exp:
            if ch == "(":
                left.append(ch)
            elif ch == ")":
                left.pop()
    except IndexError:
        return False

    if len(left) != 0:
        return False

    return True

def basic_translate(exp):
    """
    Translates basic mathematical operations (does not include functions)
    Does not translate parentheses
    """

    for order in xrange(3):
        i = 0
        while i < len(exp):
            modified = False

            if exp[i] == "I":
                exp[i] = "i"

            elif exp[i] == "^" and order == 0:
                power = exp.pop(i + 1)
                if power[0] == "(" and verify_validity(power[1:-1]):
                    power = power[1:-1]
                exp[i - 1] += "^{" + power + "}"
                modified = True

            elif exp[i] == "*" and order == 1:
                exp[i - 1] += " " + exp.pop(i + 1)
                modified = True

            elif exp[i] == "/" and order == 1:
                for index in [i - 1, i + 1]:
                    if exp[index][0] == "(" and verify_validity(exp[index][1:-1]):
                        exp[index] = exp[index][1:-1]
                exp[i - 1] = "\\frac{" + exp[i - 1] + "}{" + exp.pop(i + 1) + "}"
                modified = True

            if modified:
                exp.pop(i)
                i -= 1
            else:
                i += 1

    return ''.join(exp)

def generate_function(name, args):
    """
    Generate a function with the provided name and arguments
    """

    # special parsing of arguments, based on the function
    # (i.e. if information needs to be extrapolated) from the data
    if name == "hypergeom":
        for i in xrange(2):
            if args[i * 2] == "":
                args.insert(i, "0")
            else:
                args.insert(i, str(len(args[i * 2].split(","))))
    elif name == "sum":
        args = args.pop(1).split("..") + [args[0]]

    result = functions[name].split(" || ")

    if len(result) != len(args) + 1:
        raise IOError("Error: insufficient arguments provided for function " + name)

    for n in xrange(1, len(result)):
        result.insert(2 * n - 1, args[n - 1])

    return ''.join(result)

def translate(exp):
    """
    Translate a segment of Maple to LaTeX, including functions
    """

    if exp == "":
        return ""

    exp = replace_strings(exp.strip(), constraints + spacing).split()

    for i in xrange(len(exp)):
        if exp[i] in symbols:
            exp[i] = symbols[exp[i]]

    for i in xrange(len(exp)-1, -1, -1):
        if exp[i] == "(":
            r = i + exp[i:].index(")")
            piece = basic_translate(exp[i:r + 1])

            if exp[i - 1] in functions:
                i -= 1
                piece = generate_function(exp[i], parse_arguments(piece))

            exp = exp[0:i] + [piece] + exp[r + 1:]

    return basic_translate(exp)

def modify_fields(eq):
    eq.lhs = translate(eq.lhs)
    eq.factor = translate(eq.fields["factor"])
    eq.front = translate(eq.fields["front"])

    if eq.eq_type == "series":
        eq.general = translate(eq.general[0])

    elif eq.eq_type == "contfrac":
        eq.general = parse_brackets(eq.general[0])[0]

        if eq.begin != "":
            eq.begin = parse_brackets(eq.begin)

def make_equation(eq):
    """
    Make a LaTeX equation based on a MapleEquation object
    """

    modify_fields(eq)

    equation = "\\begin{equation*}\\tag{" + eq.label + "}\n  " + eq.lhs + "\n  = "

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
                equation += make_frac(piece) + "\\subplus"
                start += 1

        if eq.factor != "":
            if eq.factor == "-1":
                equation += "-"
            else:
                equation += eq.factor + " "

        if eq.general != ["0", "1"]:
            equation += "\\CFK{m}{" + str(start) + "}{\\infty}@@{" + translate(eq.general[0]) + "}{" + \
                        translate(eq.general[1]) + "}"
        else:
            equation += "\\dots"

    # adds metadata
    equation += "\n  %  \\constraint{$" + translate(eq.constraints) + "$}"
    equation += "\n  %  \\category{" + eq.category + "}"
    equation += "\n\\end{equation*}"

    return replace_strings(equation, special)
