"""

    Started by Divya Gandla, Version Without Regex by Kevin Chen
    DRMF Project: Converting Mathematica to LaTeX

    http://www.wolframfoundation.org/programs/eCF_Identities.pdf

"""

__author__ = 'Kevin Chen'
__status__ = 'Development'
__credits__ = ["Divya Gandla", "Kevin Chen"]

import os

DIR_NAME = os.path.dirname(os.path.realpath(__file__)) + '/../data/'

SYMBOLS = {
    'Alpha': 'alpha', 'Beta': 'beta', 'Gamma': 'gamma', 'Delta': 'delta',
    'Epsilon': 'epsilon', 'Zeta': 'zeta', 'Eta': 'eta', 'Theta': 'theta',
    'Iota': 'iota', 'Kappa': 'kappa', 'Lambda': 'lambda', 'Mu': 'mu',
    'Nu': 'nu', 'Xi': 'xi', 'Omicron': 'o', 'Pi': 'pi', 'Rho': 'rho',
    'Sigma': 'sigma', 'Tau': 'tau', 'Upsilon': 'upsilon', 'Phi': 'phi',
    'Chi': 'chi', 'Psi': 'phi', 'Omega': 'omega',

    'CapitalAlpha': ' A', 'CapitalBeta': ' B', 'CapitalGamma': 'Gamma',
    'CapitalDelta': 'Delta', 'CapitalEpsilon': 'E', 'CapitalZeta': ' Z',
    'CapitalEta': ' H', 'CapitalTheta': 'Theta', 'CapitalIota': ' I',
    'CapitalKappa': 'K', 'CapitalLambda': 'Lambda', 'CapitalMu': ' M',
    'CapitalNu': ' N', 'CapitalXi': 'Xi', 'CapitalOmicron': 'O',
    'CapitalPi': 'Pi', 'CapitalRho': ' P', 'CapitalSigma': 'Sigma',
    'CapitalTau': ' T', 'CapitalUpsilon': ' Y', 'CapitalPhi': 'Phi',
    'CapitalChi': ' X', 'CapitalPsi': 'Psi', 'CapitalOmega': 'Omega',

    'CurlyEpsilon': 'varepsilon', 'CurlyTheta': 'vartheta',
    'CurlyKappa': 'varkappa', 'CurlyPi': 'varpi', 'CurlyRho': 'varrho',
    'FinalSigma': 'varsigma', 'CurlyPhi': 'varphi',
    'CurlyCapitalUpsilon': 'varUpsilon',

    'Aleph': 'aleph', 'Bet': 'beth', 'Gimel': 'gimel', 'Dalet': 'daleth',

    'Infinity': 'infty'}

LEFT_BRACKETS = list('([{')
RIGHT_BRACKETS = list(')]}')
TRIG_OUTER = ('ArcCos', 'ArcCosh', 'ArcCot', 'ArcCoth', 'ArcCsc', 'ArcCsch',
              'ArcSec', 'ArcSech', 'ArcSin', 'ArcSinh', 'ArcTan', 'ArcTanh',
              'Sinc')
TRIG_INNER = ('Cos', 'Cot', 'Csc', 'Sec', 'Sin', 'Tan',
              'Cosh', 'Coth', 'Csch', 'Sech', 'Sinh', 'Tanh')
E_EXCEPT = ('EulerGamma', 'Epsilon', 'EulerConstant', 'EulerBeta',
            'ExpIntn', 'ExpInti', 'CompEllIntE', 'CompEllIntK')


def find_surrounding(line, function, ex=(), start=0):
    # (str, str(, tuple, int)) -> tuple
    """
    Finds the indices of the beginning and end of a function; this is the main
    function that powers the converter.

    :param line: line with functions that are going to be searched
    :param function: the function you're trying to find the surrounding
                     brackets for
    :param ex: exceptions that shouldn't be converted, because conversions do
               not see if a function is a part of another function (e.g. the
               function "NotEquals" could get converted if a program was told
               the original is "Equals"
    :param start: index of where to start finding (used if there are multiple
                  of one function in a line
    :returns: positions of opening and ending brackets
    """
    positions = [0, 0]
    line = line[start:]
    positions[0] = line.find(function)

    # Finds the exceptions (if any) and returns indeces after the exception
    if ex != '' and len(ex) >= 1:
        for e in ex:
            if (line.find(e) != -1 and
                line.find(e) <= positions[0] and
                    line.find(e) + len(e) >= positions[0] + len(function)):
                return [line.find(e) + len(e) + start,
                        line.find(e) + len(e) + start]

    # Finds the start and end of a function
    count = 0
    for j in range(positions[0] + len(function), len(line) + 1):

        if line[j] in list('([{'):
            count += 1
        if line[j] in list(')]}'):
            count -= 1
        if count == 0:
            if j == positions[0] + len(function):
                positions[0] = positions[1]
            else:
                positions[1] = j + 1
            break

    return positions[0] + start, positions[1] + start


def arg_split(line, sep):
    # (str, str) -> list
    """
    Works very much like 'split', but does not split when the separator is
    inside parentheses, brackets, or braces. Useful for nested statements.

    :param line: line to be split
    :param sep: seperator (character)
    :returns: list of segments
    """
    args = []
    count = i = 0
    end = len(line) + 1
    line = line + sep

    while i != end:
        if line[i] in LEFT_BRACKETS:
            count += 1
        if line[i] in RIGHT_BRACKETS:
            count -= 1
        if count == 0 and line[i] == sep:
            args.append(line[:i])
            end -= i + 1
            line = line[i + 1:]
            i = 0
        else:
            i += 1

    return args


def search(line, i, sign, direction=-1):
    # (str, list, str(, int)) -> int
    """
    Searches for the ends of fractions or carats; excludes signs in brackets

    :param line: line to be searched
    :param i: the starting point, usually a "/" or a "^"
    :param sign: list of excluding symbols
    :param direction: direction of search, left: -1, right: 1
    :returns: indice of end
    """
    j = i + direction
    if direction == -1:
        end = -1
    else:
        end = len(line)
    count = 0

    for j in range(i + direction, end, direction):
        if line[j] in LEFT_BRACKETS:
            count += direction
        if line[j] in RIGHT_BRACKETS:
            count -= direction
        if count == 0 and line[j] in sign:
            count -= 1
        if count < 0:
            break
        if count == 0 and j == end - direction:
            j += direction
            break

    if direction == 1:
        j -= 1

    return j


def process_references(pathr):
    # (str) -> dict
    """
    Opens references file and process it into a dictionary

    :param pathr: directory of file to be read from
    :return: dictionary of processed references
    """
    with open(pathr) as refs:
        references = list(line.split('\n') for line in
                          refs.read().split('\n\n'))

    key = []
    value = []
    for pair in references:
        key.append(pair[0][3:-1].replace('"', ''))
        value.append('&'.join(pair[1:]))

    return dict(zip(key, value))


def master_function(line, params):
    # (str, tuple) -> str
    """
    A master function, reads in the conversion templates from the 'functions'
    file and performs the conversion.

    :param line: line to be converted
    :param params: tuple containing Mathematica function, equivalent LaTeX
                   function, the format, using "-" as argument placings, and
                   exceptions, if any
    :returns: converted line
    """
    m, l, sep, ex = params[:5]
    sep = [i.split('-') for i in sep]
    multi = list('+-*/')
    for _ in range(line.count(m)):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, m, ex=ex)
        else:
            pos = find_surrounding(line, m, ex=ex,
                                   start=pos[0] + (0, len(l) + 1)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + len(m) + 1:pos[1] - 1], ',')

            # Special functions that change the order of arguments:
            if m == 'GegenbauerC':
                args[0], args[1] = args[1], args[0]
            if m == 'HarmonicNumber' and len(args) == 2:
                args[0], args[1] = args[1], args[0]
            if m == 'LaguerreL' and len(args) == 3:
                args[0], args[1] = args[1], args[0]
            if m in ('HypergeometricPFQ', 'QHypergeometricPFQ'):
                if args[1] == '{}':
                    args.insert(0, 0)
                else:
                    args.insert(0, len(arg_split(args[1][1:-1], ',')))
                if args[1] == '{}':
                    args.insert(0, 0)
                else:
                    args.insert(0, len(arg_split(args[1][1:-1], ',')))

            # If the arguments in a trig function are more than one variable,
            # then instead of "@@" make it "@"
            if (m in TRIG_OUTER or m in TRIG_INNER) and \
                    sum([args[0].count(element) for element in multi]) != 0:
                sep[0][0] = sep[0][0].replace('@@', '@')

            # Add parens around ambiguous functions (trig functions)
            if m in TRIG_OUTER and len(line) != pos[1] and line[pos[1]] == '^':
                line = line[:pos[0]] + '(' + l + \
                       '%s'.join(sep[[len(y) for y in sep]
                                 .index(len(args) + 1)]) + ')' + line[pos[1]:]
            # Add the inner square, like \cos^2{x}
            elif m in TRIG_INNER and len(line) != pos[1] and \
                    line[pos[1]] == '^':
                if line[pos[1] + 1] == '{' and line[pos[1] + 3] == '}':
                    line = line[:pos[0]] + l + line[pos[1]:pos[1] + 4] + \
                           '%s'.join(sep[[len(y) for y in sep].
                                     index(len(args) + 1)]) + line[pos[1] + 4:]
                else:
                    line = line[:pos[0]] + '(' + l + \
                           '%s'.join(sep[[len(y) for y in sep].
                                     index(len(args) + 1)]) + ')' + \
                           line[pos[1]:]
            else:
                line = line[:pos[0]] + l + \
                       '%s'.join(sep[[len(y) for y in sep].
                                 index(len(args) + 1)]) + line[pos[1]:]
            line %= tuple(args)

    return line


def remove_inactive(line):
    # (str) -> str
    """
    Removes 'Inactive' and its surrounding brackets.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Inactive')):
        pos = find_surrounding(line, 'Inactive')
        if pos[0] != pos[1]:
            line = line[:pos[0]] + line[pos[0] + 9:pos[1] - 1] + line[pos[1]:]

    return line


def remove_conditionalexpression(line):
    # (str) -> str
    """
    Removes 'ConditionalExpression' and its surrounding brackets.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('ConditionalExpression')):
        pos = find_surrounding(line, 'ConditionalExpression')
        if pos[0] != pos[1]:
            line = line[:pos[0]] + line[pos[0] + 22:pos[1] - 1] + line[pos[1]:]

    return line


def remove_symbol(line):
    # (str) -> str
    """
    Removes 'Symbol' and its surrounding brackets.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Symbol')):
        pos = find_surrounding(line, 'Symbol')
        if pos[0] != pos[1]:
            line = line[:pos[0]] + line[pos[0] + 7:pos[1] - 1] + line[pos[1]:]

    return line


def carat(line):
    # (str) -> str
    """
    Converts carats ('^') to ones with braces instead of parentheses. e.g:
    'a ^ (b + c)' would only show the first character 'b' as superscript in
                  LaTeX, but converting it to
    'a ^ {b + c}' would make it look correct in LaTeX, with 'b + c' as the
                  superscript.

    :param line: line to be converted
    :returns: converted line
    """
    i = 0

    while i != len(line):
        if line[i] == '^':
            k = search(line, i, list('*/+-=, '), 1)
            if line[i + 1] == '(' and line[k] == ')':
                line = line[:i] + '^{' + line[i + 2:k] + '}' + line[k + 1:]
            else:
                line = line[:i] + '^{' + line[i + 1:k + 1] + '}' + line[k + 1:]

        i += 1

    return line


def beta(line):
    # (str) -> str
    """
    Converts Mathematica's 'Beta' function to the equivalent LaTeX macro,
    taking into account the variations for the different number of arguments.

    :param line: line to be convertedmathematica_to_latex.py:324
    :returns: converted line
    """
    for _ in range(line.count('Beta')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'Beta',
                                   ex=('BetaRegularized', '[Beta]'))
        else:
            pos = find_surrounding(line, 'Beta',
                                   ex=('BetaRegularized', '[Beta]'),
                                   start=pos[0] + (0, 9)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 5:pos[1] - 1], ',')
            if len(args) == 2:
                line = (line[:pos[0]] + '\\EulerBeta@{{{0}}}{{{1}}}'
                        .format(args[0], args[1]) + line[pos[1]:])
            else:
                line = (line[:pos[0]] + '\\IncBeta{{{0}}}@{{{1}}}{{{2}}}'
                        .format(args[0], args[1], args[2]) + line[pos[1]:])

    return line


def cfk(line):
    # (str) -> str
    """
    Converts Mathematica's 'ContinuedFractionK' to the equivalent LaTeX macro.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('ContinuedFractionK')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'ContinuedFractionK', ex='')
        else:
            pos = find_surrounding(line, 'ContinuedFractionK', ex='',
                                   start=pos[0] + (0, 5)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 19:pos[1] - 1], ',')
            moreargs = arg_split(args[-1][1:-1], ',')
            if len(args) == 3:
                line = (line[:pos[0]] +
                        '\\CFK{{{0}}}{{{1}}}{{{2}}}@@{{{3}}}{{{4}}}'
                        .format(moreargs[0], moreargs[1], moreargs[2],
                                args[0], args[1]) + line[pos[1]:])
            else:
                line = (line[:pos[0]] +
                        '\\CFK{{{0}}}{{{1}}}{{{2}}}@@{{1}}{{{3}}}'
                        .format(moreargs[0], moreargs[1], moreargs[2],
                                args[0]) + line[pos[1]:])

    return line


def gamma(line):
    # (str) -> str
    """
    Converts Mathematica's 'Gamma' function to the equivalent LaTeX macro,
    taking into account the variations for the different number of arguments.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Gamma')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'Gamma',
                                   ex=('PolyGamma', 'CapitalGamma', 'LogGamma',
                                       'EulerGamma', 'IncGamma', 'Gamma]',
                                       'GammaQ', 'GammaRegularized',
                                       'StieltjesGamma'))
        else:
            pos = find_surrounding(line, 'Gamma',
                                   ex=('PolyGamma', 'CapitalGamma', 'LogGamma',
                                       'EulerGamma', 'IncGamma', 'Gamma]',
                                       'GammaQ', 'GammaRegularized',
                                       'StieltjesGamma'),
                                   start=pos[0] + (0, 11)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 6:pos[1] - 1], ',')
            if len(args) == 1:
                line = (line[:pos[0]] + '\\EulerGamma@{{{0}}}'
                        .format(args[0]) + line[pos[1]:])
            elif len(args) == 2:
                line = (line[:pos[0]] + '\\IncGamma@{{{0}}}{{{1}}}'
                        .format(args[0], args[1]) + line[pos[1]:])
            else:
                line = (line[:pos[0]] + '\\Incgamma@{{{0}}}{{{1}}} - '
                        .format(args[0], args[1]) + '\\Incgamma@{{{0}}}{{{1}}}'
                        .format(args[0], args[2]) + line[pos[1]:])

    return line.replace('Incgamma', 'IncGamma')
    # needed or the addition of an 'IncGamma' would screw up the rest


def integrate(line):
    # (str) -> str
    """
    Converts Mathematica's 'Integrate' function to the equivalent LaTeX macro.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Integrate')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'Integrate', ex='')
        else:
            pos = find_surrounding(line, 'Integrate', ex='',
                                   start=pos[0] + (0, 10)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 10:pos[1] - 1], ',')
            moreargs = arg_split(args[1][1:-1], ',')
            line = (line[:pos[0]] + '\\int_{{{1}}}^{{{2}}}{{{3}}}d{{{0}}}'
                    .format(moreargs[0], moreargs[1], moreargs[2], args[0]) +
                    line[pos[1]:])

    return line


def legendrep(line):
    # (str) -> str
    """
    Converts Mathematica's 'LegendreP' function to the equivalent LaTeX macro,
    taking into account the variations for the different number of arguments.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('LegendreP')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'LegendreP', ex='')
        else:
            pos = find_surrounding(line, 'LegendreP', ex='',
                                   start=pos[0] + (0, 10)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 10:pos[1] - 1], ',')
            if len(args) == 2:
                line = (line[:pos[0]] + '\\LegendreP{{{0}}}@{{{1}}}'
                        .format(args[0], args[1]) + line[pos[1]:])
            else:
                # len(args) == 4
                if args[2] in ('1', '2'):
                    line = (line[:pos[0]] + '\\FerrersP[{1}]{{{0}}}@{{{2}}}'
                            .format(args[0], args[1], args[3]) + line[pos[1]:])
                else:
                    # args[2] == 3
                    line = (line[:pos[0]] + '\\LegendreP[{1}]{{{0}}}@{{{2}}}'
                            .format(args[0], args[1], args[3]) + line[pos[1]:])

    return line


def legendreq(line):
    # (str) -> str
    """
    Converts Mathematica's 'LegendreQ' function to the equivalent LaTeX macro,
    taking into account the variations for the different number of arguments.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('LegendreQ')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'LegendreQ', ex='')
        else:
            pos = find_surrounding(line, 'LegendreQ', ex='',
                                   start=pos[0] + (0, 10)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 10:pos[1] - 1], ',')
            if len(args) == 2:
                line = (line[:pos[0]] + '\\LegendreQ{{{0}}}@{{{1}}}'
                        .format(args[0], args[1]) + line[pos[1]:])
            else:
                # len(args) == 4
                if args[2] in ('1', '2'):
                    line = (line[:pos[0]] + '\\FerrersQ[{1}]{{{0}}}@{{{2}}}'
                            .format(args[0], args[1], args[3]) + line[pos[1]:])
                else:
                    # args[2] == 3
                    line = (line[:pos[0]] + '\\LegendreQ[{1}]{{{0}}}@{{{2}}}'
                            .format(args[0], args[1], args[3]) + line[pos[1]:])

    return line


def polyeulergamma(line):
    # (str) -> str
    """
    Converts Mathematica's 'Polygamma' function to the equivalent LaTeX macro,
    taking into account the variations for the different number of arguments.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('PolyGamma')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'PolyGamma', ex='')
        else:
            pos = find_surrounding(line, 'PolyGamma', ex='',
                                   start=pos[0] + (0, 10)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 10:pos[1] - 1], ',')
            if len(args) == 2:
                line = (line[:pos[0]] + '\\polygamma{{{0}}}@{{{1}}}'
                        .format(args[0], args[1]) + line[pos[1]:])
            else:
                line = (line[:pos[0]] + '\\digamma@{{{0}}}'
                        .format(args[0]) + line[pos[1]:])

    return line


def product(line):
    # (str) -> str
    """
    Converts Mathematica's product sum function to the equivalent LaTeX macro.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Product')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'Product', ex='')
        else:
            pos = find_surrounding(line, 'Product', ex='',
                                   start=pos[0] + (0, 6)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 8:pos[1] - 1], ',')
            moreargs = arg_split(args[-1][1:-1], ',')
            line = (line[:pos[0]] + '\\Prod{{{0}}}{{{1}}}{{{2}}}@{{{3}}}'
                    .format(moreargs[0], moreargs[1], moreargs[2], args[0]) +
                    line[pos[1]:])

    return line


def qpochhammer(line):
    # (str) -> str
    """
    Converts Mathematica's 'QPochhammer' function to the equivalent LaTeX
    macro.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('QPochhammer')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'QPochhammer', ex='')
        else:
            pos = find_surrounding(line, 'QPochhammer', ex='',
                                   start=pos[0] + (0, 13)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 12:pos[1] - 1], ',')

            if len(args) == 1:
                line = (line[:pos[0]] + '\\qPochhammer{{{0}}}{{{1}}}{2}'
                        .format(args[0], args[0], '{\\infty}') + line[pos[1]:])
            elif len(args) == 2:
                line = (line[:pos[0]] + '\\qPochhammer{{{0}}}{{{1}}}{2}'
                        .format(args[0], args[1], '{\\infty}') + line[pos[1]:])
            else:  # len(args) = 3
                line = (line[:pos[0]] + '\\qPochhammer{{{0}}}{{{1}}}{{{2}}}'
                        .format(args[0], args[1], args[2]) + line[pos[1]:])

    return line


def summation(line):
    # (str) -> str
    """
    Converts Mathematica's summation function to the equivalent LaTeX macro.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Sum')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'Sum', ex='')
        else:
            pos = find_surrounding(line, 'Sum', ex='',
                                   start=pos[0] + (0, 5)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 4:pos[1] - 1], ',')
            moreargs = arg_split(args[-1][1:-1], ',')
            line = (line[:pos[0]] + '\\Sum{{{0}}}{{{1}}}{{{2}}}@{{{3}}}'
                    .format(moreargs[0], moreargs[1], moreargs[2], args[0]) +
                    line[pos[1]:])

    return line


def constraint(line):
    # (str) -> str
    """
    Converts Mathematica's 'Element', 'NotElement', and 'Inequality' functions
    to LaTeX formatting using \\constraint{}.

    :param line: line to be converted
    :returns: converted line
    """
    sections = arg_split(line, ',')

    if len(sections) in (1, 0):
        return line

    constraints = arg_split(sections[-1].replace('&&', '&'), '&')

    for i, element, in enumerate(constraints):
        if i == 0:
            constraints[i] = ('\n%  \\constraint{$' +
                              element.replace('&', ' \\land '))
        else:
            constraints[i] = ('\n%    & $' +
                              element.replace('&', ' \\land '))
        if i == len(constraints) - 1:
            constraints[i] += '$}'
        else:
            constraints[i] += '$'

    line = sections[0] + ''.join(constraints)

    mathematica_elements = ('Complexes', 'Wholes', 'Naturals', 'Integers',
                            'Irrationals', 'Reals', 'Rational', 'Primes')
    latex_elements = ('Complex', 'Whole', 'NatNumber', 'Integer',
                      'Irrational', 'Real', 'Rational', 'Prime')

    for _ in range(line.count('Element')):

        try:
            pos1
        except NameError:
            pos1 = find_surrounding(line, 'Element', ex=('NotElement',))
        else:
            pos1 = find_surrounding(line, 'Element', ex=('NotElement',),
                                    start=pos1[0] + (0, 8)
                                    [(1, 0).index(pos1[1] == pos1[0])])

        if pos1[0] != pos1[1]:
            sep = arg_split(line[pos1[0] + 8:pos1[1] - 1], ',')
            sep[1] = latex_elements[mathematica_elements.index(sep[1])]
            line = (line[:pos1[0]] + sep[0].replace('|', ',') + ' \\in \\' +
                    sep[1] + line[pos1[1]:])

    for _ in range(line.count('NotElement')):

        try:
            pos2
        except NameError:
            pos2 = find_surrounding(line, 'NotElement', ex=())
        else:
            pos2 = find_surrounding(line, 'NotElement', ex=(),
                                    start=pos2[0] + (0, 11)
                                    [(1, 0).index(pos2[1] == pos2[0])])

        if pos2[0] != pos2[1]:
            sep = arg_split(line[pos2[0] + 11:pos2[1] - 1], ',')
            sep[1] = latex_elements[mathematica_elements.index(sep[1])]
            line = (line[:pos2[0]] + sep[0].replace('|', ',') +
                    ' \\notin \\' + sep[1] + line[pos2[1]:])

    for _ in range(line.count('Inequality')):
        pos3 = find_surrounding(line, 'Inequality')
        line = (line[:pos3[0]] +
                ''.join(line[pos3[0] + 11:pos3[1] - 1].split(',')) +
                line[pos3[1]:])

    return line


def convert_fraction(line):
    # (str) -> str
    """
    Converts Mathematica fractions, which are only '/', to LaTeX
    \\frac{}{}-ions.

    :param line: line to be converted
    :returns: converted line
    """
    i = 0
    sign = list('*+-=,<>&')

    while i != len(line):
        if line[i] == '/':

            j = search(line, i, sign)
            k = search(line, i, sign, 1)

            # Removes extra surrounding parentheses, if there are any.
            # This won't work if you're doing "( )( )/( )( )": it will
            # incorrectly change it to " )( / )( ", but there are no cases of
            # this happening yet, so I have not gone to fixing this yet.
            if (line[j + 1] == '(' and line[i - 1] == ')' and
                    line[i + 1] == '(' and line[k] == ')'):
                # ()/()
                line = '{0}\\frac{{{1}}}{{{2}}}{3}' \
                    .format(line[:j + 1], line[j + 2:i - 1],
                            line[i + 2:k], line[k + 1:])
            elif line[j + 1] == '(' and line[i - 1] == ')':
                # ()/--
                line = '{0}\\frac{{{1}}}{{{2}}}{3}' \
                    .format(line[:j + 1], line[j + 2:i - 1],
                            line[i + 1:k + 1], line[k + 1:])
            elif line[i + 1] == '(' and line[k] == ')':
                # --/()
                line = '{0}\\frac{{{1}}}{{{2}}}{3}' \
                    .format(line[:j + 1], line[j + 1:i],
                            line[i + 2:k], line[k + 1:])
            else:
                # --/--
                line = '{0}\\frac{{{1}}}{{{2}}}{3}' \
                    .format(line[:j + 1], line[j + 1:i],
                            line[i + 1:k + 1], line[k + 1:])
        i += 1

    return line


def piecewise(line):
    # (str) -> str
    """
    Converts Mathematica's piecewise function to LaTeX, using 'cases'.

    :param line: line to be converted
    :returns: converted line
    """
    for _ in range(line.count('Piecewise')):
        try:
            pos
        except NameError:
            pos = find_surrounding(line, 'Piecewise', ex='')
        else:
            pos = find_surrounding(line, 'Piecewise', ex='',
                                   start=pos[0] + (0, 15)
                                   [(1, 0).index(pos[1] == pos[0])])

        if pos[0] != pos[1]:
            args = arg_split(line[pos[0] + 10:pos[1] - 1], ',')

            piece = ' \\\\ '.join([' & '.join(arg_split(i[1:-1], ','))
                                   for i in arg_split(args[0][1:-1], ',')])

            if len(args) == 1:
                piece += ' \\\\ 0 & \\text{True}'
            else:
                piece += ' \\\\ ' + args[1] + ' & \\text{True}'

            line = (line[:pos[0]] + '{\\begin{cases} ' + piece +
                    ' \\end{cases}}' + line[pos[1]:])

    return line


def replace_operators(line):
    # (str) -> str
    """
    Replaces basic operators.

    :param line: line to be converted
    :returns: converted line
    """
    line = line.replace('==', '=')
    line = line.replace('!=', ' \\ne ')
    line = line.replace('||', ' \\lor ')
    line = line.replace('>=', ' \\geq ')
    line = line.replace('<=', ' \\leq ')
    line = line.replace('LessEqual', ' \\leq ')
    line = line.replace('Less', '<')
    line = line.replace('>', ' > ')
    line = line.replace('<', ' < ')
    line = line.replace('=', ' = ')
    line = line.replace('^', ' ^ ')
    line = line.replace('*', ' ')
    line = line.replace('+', ' + ')
    line = line.replace('-', ' - ')
    line = line.replace(',', ', ')

    # This is so that things in a constraint, which is denoted by percentage
    # signs, don't get operators converted
    if '%' in line:
        parts = (line[:line.index('%')], line[line.index('%'):])
        line = parts[0]
        line = line.replace('(', '\\left( ')
        line = line.replace(')', ' \\right)')
        line = line.replace('  ', ' ')
        line += parts[1]
    else:
        line = line.replace('(', '\\left( ')
        line = line.replace(')', ' \\right)')
        line = line.replace('  ', ' ')

    line = line.replace('"a"', 'a')
    line = line.replace('Catalan', '\\CatalansConstant')
    line = line.replace('GoldenRatio', '\\GoldenRatio')
    line = line.replace('Pi', '\\pi')
    line = line.replace('CalculateData`Private`nu', '\\nu')
    line = line.replace('\\Jacobisn@{t}{m ^ {2}} ^ {2}',
                        '\\Jacobisn^{2}@{t}{m ^ {2}}')

    # Replaces "E" constant with "\\expe"
    for word in E_EXCEPT:
        line = line.replace(word, word.replace('E', 'A'))
    line = line.replace('E', '\\expe')
    for word in E_EXCEPT:
        line = line.replace(word.replace('E', 'A'), word)

    return line


def replace_vars(line):
    # (str) -> str
    """
    Replaces the easy to convert variables in Mathematica to its equivalent
    LaTeX code in the dictionary 'symbols'.

    :param line: line to be converted
    :returns: converted line
    """
    for word in SYMBOLS:
        if SYMBOLS[word][0] == ' ':
            line = line.replace('\\[' + word + ']', SYMBOLS[word][1:])
        elif word == 'Infinity':
            line = line.replace('Infinity', '\\infty')
        else:
            line = line.replace('[' + word + ']', SYMBOLS[word])

    return line


def main(pathw=DIR_NAME + 'newIdentities.tex',
         pathr=DIR_NAME + 'Identities.m',
         pathref=DIR_NAME + 'References.txt'):
    # ((str, str)) -> None
    """
    Opens Mathematica file with identities and puts converted lines into
    newIdentities.tex.

    :param pathw: directory of file to be written to
    :param pathr: directory of file to be read from
    :param pathref: directory of file with references to be inserted
    :returns: None
    """
    references = process_references(pathref)

    with open(pathw, 'w') as latex:
        with open(pathr, 'r') as mathematica:

            latex.write('\n\\documentclass{article}\n\n'
                        '\\usepackage{amsmath}\n'
                        '\\usepackage{amsfonts}\n'
                        '\\usepackage{amssymb}\n'
                        '\\usepackage{breqn}\n'
                        '\\usepackage{DLMFmath}\n'
                        '\\usepackage{DRMFfcns}\n'
                        '\\usepackage[paperwidth=15in, paperheight=20in, '
                        'margin=0.5in]{geometry}\n\n'
                        '\\begin{document}\n\n\n')

            for line in mathematica:
                line = line.replace('\n', '')

                if '(*' in line and '*)' in line:
                    mtt = line[4:-3].replace('"', '')
                    line = '\\begin{equation}'
                    latex.write(line + '\n')
                else:
                    line = line.replace(' ', '')

                    line = remove_inactive(line)
                    line = remove_conditionalexpression(line)
                    line = remove_symbol(line)

                    line = line.replace('EulerGamma', '\\EulerConstant')

                    line = carat(line)

                    for func in FUNCTION_CONVERSIONS:
                        line = master_function(line, func)

                    line = beta(line)
                    line = cfk(line)
                    line = gamma(line)
                    line = integrate(line)
                    line = legendrep(line)
                    line = legendreq(line)
                    line = polyeulergamma(line)
                    line = product(line)
                    line = qpochhammer(line)
                    line = summation(line)

                    line = convert_fraction(line)
                    line = constraint(line)
                    line = piecewise(line)
                    line = replace_operators(line)
                    line = replace_vars(line)

                    if line != '':
                        line += '\n%  \\mathematicatag{$\\tt{' + mtt + '}$}'
                        try:
                            line += '\n%  \\mathematicareference{$\\text{' + \
                                    references[mtt] + '}$}'
                        except KeyError:
                            pass
                        line = '  ' + line + '\n\\end{equation}'

                    print line
                    latex.write(line + '\n')

            latex.write('\n\n\\end{document}\n')


# Open data/functions, and process the data into a comprehensible tuple that
# gets fed into the "master_function" function
with open(DIR_NAME + 'functions') as functions:
    FUNCTION_CONVERSIONS = list(arg_split(line.replace(' ', ''), ',') for line
                                in functions.read().split('\n')
                                if (line != '' and '#' not in line))

for index, item in enumerate(FUNCTION_CONVERSIONS):
    FUNCTION_CONVERSIONS[index][2] = \
        tuple(arg_split(FUNCTION_CONVERSIONS[index][2][1:-1], ','))

    if FUNCTION_CONVERSIONS[index][3] == '()':
        FUNCTION_CONVERSIONS[index][3] = ''
    else:
        FUNCTION_CONVERSIONS[index][3] = \
            tuple(FUNCTION_CONVERSIONS[index][3][1:-1].split(','))

    FUNCTION_CONVERSIONS[index] = tuple(FUNCTION_CONVERSIONS[index])

FUNCTION_CONVERSIONS = tuple(FUNCTION_CONVERSIONS)


if __name__ == '__main__':
    main()
