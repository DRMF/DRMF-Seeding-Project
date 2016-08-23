import math_function
from unittest import TestCase


before = """
\\paragraph{Arithmetic Progression}
\\index{arithmetic progression}

\\begin{equation}\\label{eq:AL.ES.AR}
  a + (a + d) + (a + 2d) + \\dots + (a + (n-1)d)
  = na + \\tfrac{1}{2} n(n-1) d
  = \\tfrac{1}{2} n (a + \\ell)
\\end{equation}

where $\\ell$ = last term of the series = $a + (n-1)d$.

\\paragraph{Geometric Progression}
\\index{geometric progression (or series)}
"""

just_math = ["""
  a + (a + d) + (a + 2d) + \\dots + (a + (n-1)d)
  = na + \\tfrac{1}{2} n(n-1) d
  = \\tfrac{1}{2} n (a + \\ell)\n""", "\\ell", "a + (n-1)d"]

no_text = """

\\index{arithmetic progression}

\\begin{equation}\\label{eq:AL.ES.AR}
a + (a + d) + (a + 2d) + \\dots + (a + (n-1)d)
= na + \\tfrac{1}{2} n(n-1) d
= \\tfrac{1}{2} n (a + \\ell)
\\end{equation}

\\index{geometric progression (or series)}

"""



class TestMathString(TestCase):
    def test_math_string(self):
        math = math_function.math_string(before)
        self.assertEqual(just_math, math)

    def test_change_original(self):
        c_o = math_function.change_original(before, just_math)
        self.assertEqual(before, c_o)

    def test_formatting(self):
        formatted = math_function.formatting(before)
        self.assertEqual(no_text, formatted)
