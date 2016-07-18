from unittest import TestCase
from src.replace_special import replace_special


class TestReplaceSpecial(TestCase):
    def test__replace_special(self):
        tex = 'z^a = \\underbrace{z \\cdot z \\cdots z}_{n \\text{ times}} = 1 / z^{-a}.'
        result = replace_special(tex)
        self.assertEqual(tex, result)
