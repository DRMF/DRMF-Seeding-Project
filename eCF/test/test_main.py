
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from MathematicaToLaTeX import main

import os

PATHW = os.path.dirname(os.path.realpath(__file__)) + '/data/test.tex'
PATHR = os.path.dirname(os.path.realpath(__file__)) + '/data/test.m'


class TestMain(TestCase):

    def test_test(self):
        main(pathw=PATHW, pathr=PATHR, test=True)
        with open(PATHW, 'r') as l:
            latex = l.read()
        self.assertEqual(
            latex, ('\n'
                    '\\documentclass{article}\n'
                    '\n'
                    '\\usepackage{amsmath}\n'
                    '\\usepackage{amsthm}\n'
                    '\\usepackage{amssymb}\n'
                    '\\usepackage{amsfonts}\n'
                    '\\usepackage{breqn}\n'
                    '\\usepackage{DLMFmath}\n'
                    '\\usepackage{DRMFfcns}\n'
                    '\\usepackage{DLMFfcns}\n'
                    '\\usepackage{graphicx}\n'
                    '\\usepackage[paperwidth=20in, paperheight=20in, margin=0.5in]{geometry}\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\n'
                    '% {"description", number}%\n'
                    '\\begin{equation*}\n'
                    'equation\n'
                    '\\end{equation*}\n'
                    '\n'
                    '\n'
                    '\\end{document}\n'))

    def test_nottest(self):
        main(pathw=PATHW, pathr=PATHR, test=False)
        with open(PATHW, 'r') as l:
            latex = l.read()
        self.assertEqual(
            latex, ('\n'
                    '\\documentclass{article}\n'
                    '\n'
                    '\\usepackage{amsmath}\n'
                    '\\usepackage{amsthm}\n'
                    '\\usepackage{amssymb}\n'
                    '\\usepackage{amsfonts}\n'
                    '\\usepackage{breqn}\n'
                    '\\usepackage{DLMFmath}\n'
                    '\\usepackage{DRMFfcns}\n'
                    '\\usepackage{DLMFfcns}\n'
                    '\\usepackage{graphicx}\n'
                    '\\usepackage[paperwidth=20in, paperheight=20in, margin=0.5in]{geometry}\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\n'
                    '\\begin{equation*} \\tag{description, number}\n'
                    'equation\n'
                    '\\end{equation*}\n'
                    '\n'
                    '\n'
                    '\\end{document}\n'))
