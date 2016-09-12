from unittest import TestCase
from replace_special import remove_special

mismatched = """
%\\frac{q(t)}{p'(t) (p(t) - p(a))^{(\lambda/\mu)-1}}$, using Cauchy's integral
%formula for the residue, and integrating by parts. See also
  b_s
  = \\frac{1}{\mu}
    \Residue_{t=a}\left[\\frac{q(t)}{(p(t) - p(a))^{(\lambda+s)/\mu}}\\right]
%  \constraint{$s = 0,1,2,\dots$.}
"""
matched = """
%\\note{This follows from \eqref{eq:AL.xx}--\eqref{eq:AL.xx} by setting $f(t) = p(t), g(t) =
%\\frac{q(t)}{p'(t) (p(t) - p(a))^{(\lambda/\mu)-1}}$, using Cauchy's integral
%formula for the residue, and integrating by parts. See also
%\citet{Cicuta:1975:RFA}.}
  b_s
  = \\frac{1}{\mu}
    \Residue_{t=a}\left[\\frac{q(t)}{(p(t) - p(a))^{(\lambda+s)/\mu}}\\right]
%  \constraint{$s = 0,1,2,\dots$.}
"""


class TestReplaceSpecial(TestCase):
    def test__replace_special(self):
        tex = "z^a = \\underbrace{z \\cdot z \\cdots z}_{n \n \\text{ times}} = 1 / z^{-a}"
        result = remove_special(tex)
        self.assertEqual(tex.split('\n'), result)
    def test_dollar_loc(self):
        actual = remove_special(mismatched)
        self.assertEqual(mismatched.split('\n'), actual)
    def test_matching(self):
        result = remove_special(matched)
        self.assertEqual(matched.split('\n'), result)