
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from latex_constraint_modifier import main

import os

PATHR = os.path.dirname(os.path.realpath(__file__)) + '/data/in.tex'
PATHW = os.path.dirname(os.path.realpath(__file__)) + '/data/testout.tex'
PATHC = os.path.dirname(os.path.realpath(__file__)) + '/data/correctout.tex'


class TestMain(TestCase):

    def test_generation(self):
        main(PATHR, PATHW)
        with open(PATHW, 'r') as r:
            out = r.read()
        with open(PATHC, 'r') as c:
            correct = c.read()

        self.assertEqual(out, correct)
