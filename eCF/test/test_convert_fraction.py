
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from mathematica_to_latex import convert_fraction


class TestConvertFraction(TestCase):

    def test_stop(self):
        self.assertEqual(convert_fraction('a*b/c*d'), 'a*\\frac{b}{c}*d')
        self.assertEqual(convert_fraction('a+b/c+d'), 'a+\\frac{b}{c}+d')
        self.assertEqual(convert_fraction('a-b/c-d'), 'a-\\frac{b}{c}-d')
        self.assertEqual(convert_fraction('a=b/c=d'), 'a=\\frac{b}{c}=d')
        self.assertEqual(convert_fraction('a,b/c,d'), 'a,\\frac{b}{c},d')
        self.assertEqual(convert_fraction('a<b/c<d'), 'a<\\frac{b}{c}<d')
        self.assertEqual(convert_fraction('a>b/c>d'), 'a>\\frac{b}{c}>d')
        self.assertEqual(convert_fraction('a&b/c&d'), 'a&\\frac{b}{c}&d')

    def test_paren(self):
        self.assertEqual(convert_fraction('a*(b+c)/(d+e)*f'), 'a*\\frac{b+c}{d+e}*f')
        self.assertEqual(convert_fraction('a+(b+c)/(d+e)+f'), 'a+\\frac{b+c}{d+e}+f')
        self.assertEqual(convert_fraction('a-(b+c)/(d+e)-f'), 'a-\\frac{b+c}{d+e}-f')
        self.assertEqual(convert_fraction('a=(b+c)/(d+e)=f'), 'a=\\frac{b+c}{d+e}=f')
        self.assertEqual(convert_fraction('a,(b+c)/(d+e),f'), 'a,\\frac{b+c}{d+e},f')
        self.assertEqual(convert_fraction('a<(b+c)/(d+e)<f'), 'a<\\frac{b+c}{d+e}<f')
        self.assertEqual(convert_fraction('a>(b+c)/(d+e)>f'), 'a>\\frac{b+c}{d+e}>f')
        self.assertEqual(convert_fraction('a&(b+c)/(d+e)&f'), 'a&\\frac{b+c}{d+e}&f')

        self.assertEqual(convert_fraction('(a)/(b)'), '\\frac{a}{b}')
        self.assertEqual(convert_fraction('a/(b)'), '\\frac{a}{b}')
        self.assertEqual(convert_fraction('(a)/b'), '\\frac{a}{b}')
        self.assertEqual(convert_fraction('a/b'), '\\frac{a}{b}')

        self.assertEqual(convert_fraction('a(b+c)/d(e+f)'), '\\frac{a(b+c)}{d(e+f)}')

    def test_none(self):
        self.assertEqual(convert_fraction('nofraction'), 'nofraction')
