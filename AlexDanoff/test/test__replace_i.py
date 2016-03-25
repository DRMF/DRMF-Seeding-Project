from unittest import TestCase
from replace_special import _replace_i as replace_i


class Test_replace_i(TestCase):
    def test__replace_i(self):
        tex = 'z^a = \\underbrace{z \\cdot z \\cdots z}_{n \\text{ times}} = 1 / z^{-a}.'
        result = replace_i(tex)
        self.assertEqual(tex, result)
