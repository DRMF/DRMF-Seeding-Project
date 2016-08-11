
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import constraint


class TestConstraint(TestCase):

    def test_single(self):
        self.assertEqual(constraint('text,Element[z,Complexes]'), 'text\n%  \constraint{$z \in \Complex$}')
        self.assertEqual(constraint('text,Element[z,Wholes]'), 'text\n%  \constraint{$z \in \Whole$}')
        self.assertEqual(constraint('text,Element[z,Naturals]'), 'text\n%  \constraint{$z \in \NatNumber$}')
        self.assertEqual(constraint('text,Element[z,Integers]'), 'text\n%  \constraint{$z \in \Integer$}')
        self.assertEqual(constraint('text,Element[z,Irrationals]'), 'text\n%  \constraint{$z \in \Irrational$}')
        self.assertEqual(constraint('text,Element[z,Reals]'), 'text\n%  \constraint{$z \in \Real$}')
        self.assertEqual(constraint('text,Element[z,Rational]'), 'text\n%  \constraint{$z \in \Rational$}')
        self.assertEqual(constraint('text,Element[z,Primes]'), 'text\n%  \constraint{$z \in \Prime$}')

    # def test_multiple(self):

    def test_none(self):
        self.assertEqual(constraint('noconstraint'), 'noconstraint')
