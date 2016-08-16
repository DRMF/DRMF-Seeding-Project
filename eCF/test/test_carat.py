
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import carat


class TestCarat(TestCase):

    def test_seperate(self):
        self.assertEqual(carat('a^b'), 'a^{b}')
        self.assertEqual(carat('a^b*c'), 'a^{b}*c')
        self.assertEqual(carat('a^b/c'), 'a^{b}/c')
        self.assertEqual(carat('a^b+c'), 'a^{b}+c')
        self.assertEqual(carat('a^b-c'), 'a^{b}-c')
        self.assertEqual(carat('a^b=c'), 'a^{b}=c')
        self.assertEqual(carat('a^b,c'), 'a^{b},c')
        self.assertEqual(carat('a^b c'), 'a^{b} c')

    def test_parentheses(self):
        self.assertEqual(carat('a^(b+c)'), 'a^{b+c}')
        self.assertEqual(carat('a^(b+c)*d'), 'a^{(b+c)}*d')
        self.assertEqual(carat('a^(b+c)/d'), 'a^{(b+c)}/d')
        self.assertEqual(carat('a^(b+c)+d'), 'a^{(b+c)}+d')
        self.assertEqual(carat('a^(b+c)-d'), 'a^{(b+c)}-d')
        self.assertEqual(carat('a^(b+c)=d'), 'a^{(b+c)}=d')
        self.assertEqual(carat('a^(b+c),d'), 'a^{(b+c)},d')

    def test_none(self):
        self.assertEqual(carat('nocarat'), 'nocarat')
