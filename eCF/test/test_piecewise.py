
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import piecewise

class TestPiecewise(TestCase):

    def test_single(self):
        self.assertEqual(piecewise(
            'Piecewise[{{var,cond}}]'),
            '{\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}}')
        self.assertEqual(piecewise(
            '--Piecewise[{{var,cond}}]--'),
            '--{\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}}--')
        self.assertEqual(piecewise(
            'Piecewise[{{var,cond}},0]'),
            '{\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}}')
        self.assertEqual(piecewise(
            '--Piecewise[{{var,cond}},0]--'),
            '--{\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}}--')
        self.assertEqual(piecewise(
            'Piecewise[{{var,cond}},num]'),
            '{\\begin{cases} var & cond \\\\ num & \\text{True} \\end{cases}}')
        self.assertEqual(piecewise(
            '--Piecewise[{{var,cond}},num]--'),
            '--{\\begin{cases} var & cond \\\\ num & \\text{True} \\end{cases}}--')

    def test_multiple(self):
        self.assertEqual(piecewise(
            'Piecewise[{{var1,cond1},{var2,cond2}},0]'),
            '{\\begin{cases} var1 & cond1 \\\\ var2 & cond2 \\\\ 0 & \\text{True} \\end{cases}}')
        self.assertEqual(piecewise(
            '--Piecewise[{{var1,cond1},{var2,cond2}},0]--'),
            '--{\\begin{cases} var1 & cond1 \\\\ var2 & cond2 \\\\ 0 & \\text{True} \\end{cases}}--')
        self.assertEqual(piecewise(
            'Piecewise[{{var1,cond1},{var2,cond2},{var3,cond3}},0]'),
            '{\\begin{cases} var1 & cond1 \\\\ var2 & cond2 \\\\ var3 & cond3 \\\\ 0 & \\text{True} \\end{cases}}')
        self.assertEqual(piecewise(
            '--Piecewise[{{var1,cond1},{var2,cond2},{var3,cond3}},0]--'),
            '--{\\begin{cases} var1 & cond1 \\\\ var2 & cond2 \\\\ var3 & cond3 \\\\ 0 & \\text{True} \\end{cases}}--')

    def test_nested(self):
        self.assertEqual(piecewise(
            'Piecewise[{{Piecewise[{{var,Piecewise[{{var,cond}}]}}],Piecewise[{{var,cond}}]}}]'),
            '{\\begin{cases} {\\begin{cases} var & {\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}} \\\\ 0 & \\text{True} \\end{cases}} & {\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}} \\\\ 0 & \\text{True} \\end{cases}}')
        self.assertEqual(piecewise(
            '--Piecewise[{{Piecewise[{{var,Piecewise[{{var,cond}}]}}],Piecewise[{{var,cond}}]}}]--'),
            '--{\\begin{cases} {\\begin{cases} var & {\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}} \\\\ 0 & \\text{True} \\end{cases}} & {\\begin{cases} var & cond \\\\ 0 & \\text{True} \\end{cases}} \\\\ 0 & \\text{True} \\end{cases}}--')

    def test_none(self):
        self.assertEqual(piecewise('nopiecewise'), 'nopiecewise')
