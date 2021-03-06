
__author__ = 'Kevin Chen'
__status__ = 'Development'

from unittest import TestCase
from mathematica_to_latex import main

import os

PATHW = os.path.dirname(os.path.realpath(__file__)) + '/data/test.tex'
PATHR = os.path.dirname(os.path.realpath(__file__)) + '/data/test.m'
PATHREF = os.path.dirname(os.path.realpath(__file__)) + '/data/testref.txt'


class TestMain(TestCase):

    def test_generation(self):
        main(pathr=PATHR, pathw=PATHW, pathref=PATHREF, verbose=True)
        with open(PATHW, 'r') as l:
            latex = l.read()
        self.assertEqual(
            latex, ('\n'
                    '\\documentclass{article}\n'
                    '\n'
                    '\\usepackage{amsmath}\n'
                    '\\usepackage{amsfonts}\n'
                    '\\usepackage{DLMFmath}\n'
                    '\\usepackage{DRMFfcns}\n'
                    '\\usepackage{amssymb}\n'
                    '\\usepackage[paperwidth=15in, paperheight=20in, margin=0.5in]{geometry}\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\\title{eCF Dataset}\n'
                    '\\section{Main}\n'
                    '\n'
                    '\\begin{equation}\n'
                    '  equation\n'
                    '%  \\mathematicatag{$\\tt{description, number}$}\n'
                    '%  \\mathematicareference{$\\text{test reference line 1&test reference line 2}$}\n'
                    '\\end{equation}\n'
                    '\n'
                    '\\begin{equation}\n'
                    '  equation\n'
                    '%  \\mathematicatag{$\\tt{nodescription, number}$}\n'
                    '\\end{equation}\n'
                    '\n'
                    '\n'
                    '\\end{document}\n'))

    def test_other(self):
        self.assertNotEqual(main(pathr=PATHR, pathw=PATHW, pathref=''), True)
        self.assertNotEqual(main(manual='test'), True)
