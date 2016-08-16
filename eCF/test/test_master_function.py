
__author__ = 'Kevin Chen'
__status__ = 'Development'

import os
from unittest import TestCase
from MathematicaToLaTeX import master_function
from MathematicaToLaTeX import arg_split


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

    def test_exception(self):
        for function in FUNCTION_CONVERSIONS:
            if function[3] != '':
                for exception in function[3]:
                    self.assertEqual(master_function(exception + '[]', function), exception + '[]')

    def test_none(self):
        for func in FUNCTION_CONVERSIONS:
            self.assertEqual(master_function('nofunction', func), 'nofunction')
