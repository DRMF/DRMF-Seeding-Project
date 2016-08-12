
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import constraint


class TestConstraint(TestCase):

    def test_element_singlevar(self):
        self.assertEqual(constraint('text,Element[a,Complexes]'),
                         'text\n'
                         '%  \constraint{$a \in \Complex$}')
        self.assertEqual(constraint('text,Element[a,Wholes]'),
                         'text\n'
                         '%  \constraint{$a \in \Whole$}')
        self.assertEqual(constraint('text,Element[a,Naturals]'),
                         'text\n'
                         '%  \constraint{$a \in \\NatNumber$}')
        self.assertEqual(constraint('text,Element[a,Integers]'),
                         'text\n'
                         '%  \constraint{$a \in \Integer$}')
        self.assertEqual(constraint('text,Element[a,Irrationals]'),
                         'text\n'
                         '%  \constraint{$a \in \Irrational$}')
        self.assertEqual(constraint('text,Element[a,Reals]'),
                         'text\n'
                         '%  \constraint{$a \in \Real$}')
        self.assertEqual(constraint('text,Element[a,Rational]'),
                         'text\n'
                         '%  \constraint{$a \in \Rational$}')
        self.assertEqual(constraint('text,Element[a,Primes]'),
                         'text\n'
                         '%  \constraint{$a \in \Prime$}')

    def test_element_multivar(self):
        self.assertEqual(constraint('text,Element[a|b|c|d,Complexes]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Complex$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Wholes]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Whole$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Naturals]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \\NatNumber$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Integers]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Integer$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Irrationals]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Irrational$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Reals]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Real$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Rational]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Rational$}')
        self.assertEqual(constraint('text,Element[a|b|c|d,Primes]'),
                         'text\n'
                         '%  \constraint{$a,b,c,d \in \Prime$}')

    def test_notelement_singlevar(self):
        self.assertEqual(constraint('text,NotElement[a,Complexes]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Complex$}')
        self.assertEqual(constraint('text,NotElement[a,Wholes]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Whole$}')
        self.assertEqual(constraint('text,NotElement[a,Naturals]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\NatNumber$}')
        self.assertEqual(constraint('text,NotElement[a,Integers]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Integer$}')
        self.assertEqual(constraint('text,NotElement[a,Irrationals]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Irrational$}')
        self.assertEqual(constraint('text,NotElement[a,Reals]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Real$}')
        self.assertEqual(constraint('text,NotElement[a,Rational]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Rational$}')
        self.assertEqual(constraint('text,NotElement[a,Primes]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Prime$}')

    def test_notelement_multivar(self):
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Complexes]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Complex$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Wholes]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Whole$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Naturals]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\NatNumber$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Integers]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Integer$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Irrationals]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Irrational$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Reals]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Real$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Rational]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Rational$}')
        self.assertEqual(constraint('text,NotElement[a|b|c|d,Primes]'),
                         'text\n'
                         '%  \\constraint{$a,b,c,d \\notin \\Prime$}')

    def test_inequality(self):
        self.assertEqual(constraint('text,Inequality[a,Less,b,LessEqual,c]'),
                         'text\n'
                         '%  \\constraint{$aLessbLessEqualc$}')

    def test_multiple(self):
        self.assertEqual(constraint('text,Element[a,Complexes]&&Element[b,Wholes]'),
                         'text\n'
                         '%  \\constraint{$a \\in \\Complex$\n'
                         '%    & $b \\in \\Whole$}')
        self.assertEqual(constraint('text,Element[a,Complexes]&&Element[b,Wholes]&&Element[c,Naturals]'),
                         'text\n'
                         '%  \\constraint{$a \\in \\Complex$\n'
                         '%    & $b \\in \\Whole$\n'
                         '%    & $c \\in \\NatNumber$}')

        self.assertEqual(constraint('text,NotElement[a,Complexes]&&NotElement[b,Wholes]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Complex$\n'
                         '%    & $b \\notin \\Whole$}')
        self.assertEqual(constraint('text,NotElement[a,Complexes]&&NotElement[b,Wholes]&&NotElement[c,Naturals]'),
                         'text\n'
                         '%  \\constraint{$a \\notin \\Complex$\n'
                         '%    & $b \\notin \\Whole$\n'
                         '%    & $c \\notin \\NatNumber$}')

        self.assertEqual(constraint('text,Inequality[a,Less,b]&&Inequality[b,Less,c]'),
                         'text\n'
                         '%  \\constraint{$aLessb$\n'
                         '%    & $bLessc$}')
        self.assertEqual(constraint('text,Inequality[a,Less,b]&&Inequality[b,Less,c]&&Inequality[c,Less,d]'),
                         'text\n'
                         '%  \\constraint{$aLessb$\n'
                         '%    & $bLessc$\n'
                         '%    & $cLessd$}')

        self.assertEqual(constraint('text,Element[a|b|c,Complexes]&&NotElement[d|e|f,Primes]&&Inequality[g,Less,h,Less,i]'),
                         'text\n'
                         '%  \\constraint{$a,b,c \\in \\Complex$\n'
                         '%    & $d,e,f \\notin \\Prime$\n'
                         '%    & $gLesshLessi$}')

    def test_none(self):
        self.assertEqual(constraint('noconstraint'), 'noconstraint')