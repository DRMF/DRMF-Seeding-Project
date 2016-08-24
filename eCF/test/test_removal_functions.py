
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from mathematica_to_latex import remove_inactive
from mathematica_to_latex import remove_conditionalexpression
from mathematica_to_latex import remove_symbol


BEFORE1 = ('Inactive[test]',
           'testInactive[test]test',
           'Inactive[testInactive[test]test]',
           'testInactive[testInactive[test]test]test')
BEFORE2 = ('ConditionalExpression[test]',
           'testConditionalExpression[test]test',
           'ConditionalExpression[testConditionalExpression[test]test]',
           'testConditionalExpression[testConditionalExpression[test]test]test')
BEFORE3 = ('Symbol[test]',
           'testSymbol[test]test',
           'Symbol[testSymbol[test]test]',
           'testSymbol[testSymbol[test]test]test')
AFTER = ('test',
         'testtesttest',
         'testtesttest',
         'testtesttesttesttest')


class TestRemovalFunctions(TestCase):

    def test_single(self):
        self.assertEqual(remove_inactive(
            BEFORE1[0]), AFTER[0])
        self.assertEqual(remove_conditionalexpression(
            BEFORE2[0]), AFTER[0])
        self.assertEqual(remove_symbol(
            BEFORE3[0]), AFTER[0])

    def test_single_withsurrounding(self):
        self.assertEqual(remove_inactive(
            BEFORE1[1]), AFTER[1])
        self.assertEqual(remove_conditionalexpression(
            BEFORE2[1]), AFTER[1])
        self.assertEqual(remove_symbol(
            BEFORE3[1]), AFTER[1])

    def test_nested_inactive(self):
        self.assertEqual(remove_inactive(
            BEFORE1[2]), AFTER[2])
        self.assertEqual(remove_conditionalexpression(
            BEFORE2[2]), AFTER[2])
        self.assertEqual(remove_symbol(
            BEFORE3[2]), AFTER[2])

    def test_nested_withsurrounding(self):
        self.assertEqual(remove_inactive(
            BEFORE1[3]), AFTER[3])
        self.assertEqual(remove_conditionalexpression(
            BEFORE2[3]), AFTER[3])
        self.assertEqual(remove_symbol(
            BEFORE3[3]), AFTER[3])
