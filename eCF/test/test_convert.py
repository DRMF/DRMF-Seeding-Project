
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from mathematica_to_latex import convert


class TestConvert(TestCase):

    def test_convert(self):
        self.assertEqual(convert('Log[a,b]'), 'Could not convert.')
