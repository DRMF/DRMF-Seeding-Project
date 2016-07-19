__author__ = "Azeem Mohammed"
__status__ = "Development"

from unittest import TestCase
from tex2Wiki import isnumber


class TestIsnumber(TestCase):
    def test_isnumber(self):
        self.assertEqual(True, isnumber("1"))
        self.assertEqual(False, isnumber("a"))
