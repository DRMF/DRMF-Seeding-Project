
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import replace_operators


class TestReplaceOperators(TestCase):

    def test_without_percent(self):
        self.assertEqual(replace_operators('=='), ' = ')
        self.assertEqual(replace_operators('||'), ' \\lor ')
        self.assertEqual(replace_operators('>='), ' \\geq ')
        self.assertEqual(replace_operators('<='), ' \\leq ')
        self.assertEqual(replace_operators('LessEqual'), ' \\leq ')
        self.assertEqual(replace_operators('Less'), ' < ')
        self.assertEqual(replace_operators('>'), ' > ')
        self.assertEqual(replace_operators('<'), ' < ')
        self.assertEqual(replace_operators('='), ' = ')
        self.assertEqual(replace_operators('^'), ' ^ ')
        self.assertEqual(replace_operators('*'), ' ')
        self.assertEqual(replace_operators('+'), ' + ')
        self.assertEqual(replace_operators('-'), ' - ')
        self.assertEqual(replace_operators(','), ', ')
        self.assertEqual(replace_operators('('), '\\left( ')
        self.assertEqual(replace_operators(')'), ' \\right)')
        self.assertEqual(replace_operators('  '), ' ')
        self.assertEqual(replace_operators('"a"'), 'a')

    def test_constants(self):
        self.assertEqual(replace_operators('Catalan'), '\\CatalansConstant')
        self.assertEqual(replace_operators('GoldenRatio'), '\\GoldenRatio')
        self.assertEqual(replace_operators('Pi'), '\\pi')
        self.assertEqual(replace_operators('CalculateData`Private`nu'), '\\text{CalculateData`Private`nu}')

    def test_with_percent(self):
        self.assertEqual(replace_operators('(%('), '\\left( %(')
        self.assertEqual(replace_operators(')%)'), ' \\right)%)')
        self.assertEqual(replace_operators('  %  '), ' %  ')

    def test_none(self):
        self.assertEqual(replace_operators(''), '')
        self.assertEqual(replace_operators('%'), '%')