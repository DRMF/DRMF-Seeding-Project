
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import arg_split


class TestArgumentSplit(TestCase):

    def test_normal(self):
        self.assertEqual(arg_split(','.join(list('abcdef')), ','), ','.join(list('abcdef')).split(','))

    def test_empty(self):
        self.assertEqual(arg_split(',,,,,,', ','), ',,,,,,'.split(','))

    def test_some_empty(self):
        before = 'a,,b,,c,,d'
        after = ['a', '', 'b', '', 'c', '', 'd']
        self.assertEqual(arg_split(before, ','), after)

    def test_parens(self):
        before = '(a,b),[c,d],{e,(f,g)}'
        after = ['(a,b)', '[c,d]', '{e,(f,g)}']
        self.assertEqual(arg_split(before, ','), after)

    def test_combined(self):
        before = 'a,(b,c),,[d,e],,,{fg,hi}'
        after = ['a', '(b,c)', '', '[d,e]', '', '', '{fg,hi}']
        self.assertEqual(arg_split(before, ','), after)

    def test_none(self):
        self.assertEqual(arg_split('noseperator', ','), ['noseperator'])
