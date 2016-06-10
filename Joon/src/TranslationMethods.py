#!/usr/bin/env python

# Constants
FUNCTIONS = dict(tuple(line.split(" || ", 1)) for line in open("keys/functions").read().split("\n")
                 if line != "" and "%" not in line)
SYMBOLS = list(line.split(" || ") for line in open("keys/symbols").read().split("\n")
               if line != "" and "%" not in line)
PARENTHESES = [["(", "\\left("], [")", "\\right)"]]
SPACING = list((char, " " + char + " ") for char in ["(", ")", "+", "-", "*", "/", "^", "<", ">", ","])
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

    return [[translate(p) for p in piece.split(", ")] for piece in exp[1:-1].split("], [")]

def make_frac(n, d):
    """
    Generate a LaTeX frac from numerator and denominator
    """

    return "\\frac{" + n + "}{" + d + "}"

def parse_arguments(pieces):
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

    for order in range(2):
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
                # rules for nicer spacing
                if exp[i - 1][-1] not in "})" and exp[i + 1][0] != "\\" \
                        or exp[i - 1][-1] in NUMBERS and exp[i + 1] in NUMBERS:
                    exp[i - 1] += " "
                exp[i - 1] += exp.pop(i + 1)
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

    exp = exp.strip()

    parens, i = list(), 0
    exp = replace_strings(exp, SYMBOLS + SPACING).split()

    while i < len(exp):
        if exp[i] == "(":
            if exp[i - 1] in FUNCTIONS:
                parens.append([i, FUNCTIONS[exp[i - 1]]])
            else:
                parens.append([i])

        elif exp[i] == ")":
            info = parens.pop()
            l = info[0]
            piece = basic_translate(exp[l:i + 1])

            if len(info) == 2:
                l -= 1
                func = info[1].split(" || ")
                piece = parse_arguments(piece)
                result = [func[-1]]
                for c in range(len(piece))[::-1]:
                    result += [piece[c], func[c]]
                piece = ''.join(result[::-1])

            exp = exp[0:l] + [piece] + exp[i + 1:]
            i = l

        i += 1

    return replace_strings(basic_translate(exp), PARENTHESES)