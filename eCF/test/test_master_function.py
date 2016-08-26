
__author__ = 'Kevin Chen'
__status__ = 'Development'

import os
from unittest import TestCase
from mathematica_to_latex import master_function
from mathematica_to_latex import arg_split


with open(os.path.dirname(os.path.realpath(__file__)) + '/../data/functions') as functions:
    FUNCTION_CONVERSIONS = list(arg_split(line.replace(' ', ''), ',') for line
                                in functions.read().split('\n')
                                if (line != '' and '#' not in line))


for index, item in enumerate(FUNCTION_CONVERSIONS):
    FUNCTION_CONVERSIONS[index][2] = tuple(arg_split(FUNCTION_CONVERSIONS[index][2][1:-1], ','))

    if FUNCTION_CONVERSIONS[index][3] == '()':
        FUNCTION_CONVERSIONS[index][3] = ''
    else:
        FUNCTION_CONVERSIONS[index][3] = tuple(FUNCTION_CONVERSIONS[index][3][1:-1].split(','))

    FUNCTION_CONVERSIONS[index] = tuple(FUNCTION_CONVERSIONS[index])

FUNCTION_CONVERSIONS = tuple(FUNCTION_CONVERSIONS)
TRIG_OUTER = ('ArcCos', 'ArcCosh', 'ArcCot', 'ArcCoth', 'ArcCsc', 'ArcCsch',
              'ArcSec', 'ArcSech', 'ArcSin', 'ArcSinh', 'ArcTan', 'ArcTanh',
              'Sinc')
TRIG_INNER = ('Cos', 'Cot', 'Csc', 'Sec', 'Sin', 'Tan',
              'Cosh', 'Coth', 'Csch', 'Sech', 'Sinh', 'Tanh')
MULTI = list('+-*/')


class TestMasterFunction(TestCase):

    def test_conversion(self):
        for function in FUNCTION_CONVERSIONS:
            for case in function[2]:
                args = list('abcdefg'[:case.count('-')])
                before = function[0] + '[' + ','.join(args) + ']'
                after = function[1] + case.replace('-', '%s')

                if function[0] == 'GegenbauerC':
                    args[0], args[1] = args[1], args[0]
                if function[0] == 'HarmonicNumber' and case.count('-') == 2:
                    args[0], args[1] = args[1], args[0]
                if function[0] == 'LaguerreL' and case.count('-') == 3:
                    args[0], args[1] = args[1], args[0]

                after %= tuple(args)

                if function[0] == 'HypergeometricPFQ':
                    self.assertEqual(master_function('HypergeometricPFQ[{},{},a]', function),
                                     '\\HyperpFq{0}{0}@@{}{}{a}')
                    self.assertEqual(master_function('--HypergeometricPFQ[{},{},a]--', function),
                                     '--\\HyperpFq{0}{0}@@{}{}{a}--')
                    self.assertEqual(master_function('HypergeometricPFQ[{a,b,c},{d,e,f},g]', function),
                                     '\\HyperpFq{3}{3}@@{a,b,c}{d,e,f}{g}')
                    self.assertEqual(master_function('--HypergeometricPFQ[{a,b,c},{d,e,f},g]--', function),
                                     '--\\HyperpFq{3}{3}@@{a,b,c}{d,e,f}{g}--')
                    self.assertEqual(master_function('HypergeometricPFQ[{},{},HypergeometricPFQ[{},{},a]]', function),
                                     '\\HyperpFq{0}{0}@@{}{}{\\HyperpFq{0}{0}@@{}{}{a}}')
                elif function[0] == 'QHypergeometricPFQ':
                    self.assertEqual(master_function('QHypergeometricPFQ[{},{},a,b]', function),
                                     '\\qHyperrphis{0}{0}@@{}{}{a}{b}')
                    self.assertEqual(master_function('--QHypergeometricPFQ[{},{},a,b]--', function),
                                     '--\\qHyperrphis{0}{0}@@{}{}{a}{b}--')
                    self.assertEqual(master_function('QHypergeometricPFQ[{a,b,c},{d,e,f},g,h]', function),
                                     '\\qHyperrphis{3}{3}@@{a,b,c}{d,e,f}{g}{h}')
                    self.assertEqual(master_function('--QHypergeometricPFQ[{a,b,c},{d,e,f},g,h]--', function),
                                     '--\\qHyperrphis{3}{3}@@{a,b,c}{d,e,f}{g}{h}--')
                else:
                    self.assertEqual(master_function(before, function), after)
                    self.assertEqual(master_function('--{0}--'.format(before), function), '--{0}--'.format(after))

                    # Test single and double "@" signs
                    if function[0] in TRIG_OUTER or function[0] in TRIG_INNER:
                        for sep in MULTI:
                            before2 = before[:-1] + sep + 'b]'
                            after2 = after.replace('@@', '@')[:-1] + sep + 'b}'
                            self.assertEqual(master_function(before2, function), after2)
                            self.assertEqual(master_function('--{0}--'.format(before2), function), '--{0}--'.format(after2))

                    # Test parentheses placement for powers in functions
                    if function[0] in TRIG_OUTER:
                        before2 = before + '^'
                        after2 = '(' + after + ')^'
                        self.assertEqual(master_function(before2, function), after2)
                        self.assertEqual(master_function('--{0}--'.format(before2), function), '--{0}--'.format(after2))
                    if function[0] in TRIG_INNER:
                        before2 = before + '^{b}'
                        after2 = after[:-5] + '^{b}@@{a}'
                        self.assertEqual(master_function(before2, function), after2)
                        self.assertEqual(master_function('--{0}--'.format(before2), function), '--{0}--'.format(after2))

                    # Test an exception
                    if function[0] == 'D':
                        self.assertEqual(master_function('\\[Delta]', function), '\\[Delta]')

    def test_exception(self):
        for function in FUNCTION_CONVERSIONS:
            if function[3] != '':
                for exception in function[3]:
                    self.assertEqual(master_function(exception + '[]', function), exception + '[]')

    def test_none(self):
        for func in FUNCTION_CONVERSIONS:
            self.assertEqual(master_function('nofunction', func), 'nofunction')
