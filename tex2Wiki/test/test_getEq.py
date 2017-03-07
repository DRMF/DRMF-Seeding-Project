from unittest import TestCase
from tex2Wiki import getEq
from tex2Wiki import setup_label_links
class TestGetEq(TestCase):

    def test_getEq(self):
        self.assertEqual('<math>\realpart{s} > 1</math>', getEq('%  \constraint{$\realpart{s} > 1$}'))
        self.assertEqual('<math>\realpart{s} > -1</math> &<br /> <math>s\neq 1</math>', getEq('%  \constraint{$\realpart{s} > -1$ &<br /> $s \neq 1$}\n'))
        self.assertEqual('<math>\realpart{s} > -1</math> &<br /> <math>s\neq 1</math>', getEq('%  \constraint{$\realpart{s} > -1$ &<br /> $s \neq 1$}'))