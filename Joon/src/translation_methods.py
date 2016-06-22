#!/usr/bin/env python

# Constants
FUNCTIONS = dict(tuple(line.split(" || ", 1)) for line in open("keys/functions").read().split("\n")
                 if line != "" and "%" not in line)
SYMBOLS = dict(tuple(line.split(" || ")) for line in open("keys/symbols").read().split("\n")
               if line != "" and "%" not in line)
SPACING = list((char, " " + char + " ") for char in ["(", ")", "+", "-", "*", "/", "^", "<", ">", ",", "::"])
SPECIAL = [["(", "\\left("], [")", "\\right)"], ["+-", "-"], ["\\subplus-", "-"]]
CONSTRAINTS = list(tuple(line.split(" || ")) for line in open("keys/constraints").read().split("\n")
                   if line != "" and "%" not in line)
NUMBERS = "0123456789"

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

    return [[translate(p) for p in piece.split(",")] for piece in exp[1:-1].split("], [")]

def make_frac(n, d):
    """
    Generate a LaTeX frac from numerator and denominator
    """

    return "\\frac{" + n + "}{" + d + "}"

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
                if power[-1] == ")":
                    power = ''.join(power[1:-1])
                exp[i - 1] += "^{" + power + "}"
                modified = True

            elif exp[i] == "*" and order == 1:
                exp[i - 1] += " " + exp.pop(i + 1)
                modified = True

            elif exp[i] == "/" and order == 1:
                for index in [i - 1, i + 1]:
                    if exp[index][0] == "(" and exp[index][-1] == ")":
                        exp[index] = exp[index][1:-1]
                exp[i - 1] = "\\frac{" + exp[i - 1] + "}{" + exp.pop(i + 1) + "}"
                modified = True

            if modified:
                exp.pop(i)
                i -= 1
            else:
                i += 1

    return ''.join(exp)

def translate(exp):
    """
    Translate a segment of Maple to LaTeX, including functions
    """

    exp = replace_strings(exp.strip(), CONSTRAINTS + [[":-", ":"]] + SPACING).split()

    for i in xrange(len(exp)):
        if exp[i] in SYMBOLS:
            exp[i] = SYMBOLS[exp[i]]

    for i in xrange(len(exp)-1, -1, -1):
        if exp[i] == "(":
            r = i + exp[i:].index(")")
            piece = basic_translate(exp[i:r + 1])

            if exp[i - 1] in FUNCTIONS:
                i -= 1
                func = FUNCTIONS[exp[i]].split(" || ")

                piece = parse_arguments(piece)

                # parsing for hypergeometric function
                if exp[i] == "hypergeom":
                    for j in xrange(2):
                        if piece[j * 2] == "":
                            piece.insert(j, "0")
                        else:
                            piece.insert(j, str(len(piece[j * 2].split(","))))

                result = [func.pop(0)] + [piece[c] + func[c] for c in xrange(len(piece))]
                piece = ''.join(result)

            exp = exp[0:i] + [piece] + exp[r + 1:]

    return basic_translate(exp)

def modify_fields(eq):
    eq.lhs = translate(eq.lhs)

    if "factor" in eq.fields:
        eq.factor = translate(eq.fields["factor"])

    if "front" in eq.fields:
        eq.front = translate(eq.fields["front"])

    if eq.eq_type == "series":
        eq.general = translate(eq.general[0])

    elif eq.eq_type == "contfrac":
        eq.general = parse_brackets(eq.general[0])  # add handling later for even and odd

        if isinstance(eq.general[0], list):
            eq.general = eq.general[0]

        if "begin" in eq.fields:
            eq.begin = parse_brackets(eq.begin)

def make_equation(eq):
    """
    Make a LaTeX equation based on a MapleEquation object
    """

    modify_fields(eq)

    equation = "\\begin{equation*}\\tag{" + eq.label + "}\n  " + eq.lhs + "\n  = "

    # translates the Maple information (with spacing)
    if eq.eq_type == "series":
        if "factor" in eq.fields:
            equation += eq.factor + " "

        elif "front" in eq.fields:
            equation += eq.front + "+"

        equation += "\\sum_{k=0}^\\infty "

        if eq.category == "power series":
            equation += eq.general
        elif eq.category == "asymptotic series":  # make sure to fix asymptotic series
            equation += "(" + eq.general + ")"

    elif eq.eq_type == "contfrac":
        start = 1  # in case the value of start isn't assigned

        if "begin" in eq.fields:
            for piece in eq.begin:
                equation += make_frac(piece[0], piece[1]) + "\\subplus"
                start += 1

        elif "front" in eq.fields:
            equation += eq.front + "+"
            start = 1

        if "factor" in eq.fields:
            if eq.factor == "-1":
                equation += "-"
            else:
                equation += eq.factor + " "

        equation += "\\CFK{m}{" + str(start) + "}{\\infty}@{" + eq.general[0] + "}{" + eq.general[1] + "}"

    # adds metadata
    equation += "\n  %  \\constraint{$" + translate(eq.constraints) + "$}"
    equation += "\n  %  \\category{" + eq.category + "}"
    equation += "\n\\end{equation*}"

    return replace_strings(equation, SPECIAL)
