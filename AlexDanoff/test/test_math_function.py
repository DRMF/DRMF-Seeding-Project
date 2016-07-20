from math_function import math_string
from unittest import TestCase

class TestMathString(TestCase):
    def test_math_string(self):
        before = """
        \paragraph{Arithmetic Progression}
        \index{arithmetic progression}

        \begin{equation}\label{eq:AL.ES.AR}
          a + (a + d) + (a + 2d) + \dots + (a + (n-1)d)
          = na + \tfrac{1}{2} n(n-1) d
          = \tfrac{1}{2} n (a + \ell)
        \end{equation}

        where $\ell$ = last term of the series = $a + (n-1)d$.

        \paragraph{Geometric Progression}
        \index{geometric progression (or series)}"""

        after = ["""a + (a + d) + (a + 2d) + \dots + (a + (n-1)d)
          = na + \tfrac{1}{2} n(n-1) d
          = \tfrac{1}{2} n (a + \ell)""", "\ell", "a + (n-1)d"]

        math = math_string(before)
        print 'math', math
        print 'after', after
        self.assertEqual(after, math)
