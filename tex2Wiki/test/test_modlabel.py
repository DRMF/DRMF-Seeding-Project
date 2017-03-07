__author__ = "Azeem Mohammed"
__status__ = "Development"

from unittest import TestCase
from tex2Wiki import mod_label
from tex2Wiki import setup_label_links


class TestModLabel(TestCase):
    def test_modLabel(self):
        self.assertEqual('Formula:EF.EX.TM', mod_label('\\begin{equation}\label{eq:EF.EX.TM}'))
        self.assertEqual('Formula:EF.EX.TM', mod_label('\\begin{equation}\\formula{eq:EF.EX.TM}'))
        self.assertEqual('auto-number-1', mod_label('\\begin{equation}'))
        self.assertEqual('auto-number-2', mod_label('\\begin{equation}'))

    def test_modLabelsWithList(self):
        setup_label_links('testdata/llinks')
        self.assertEqual('DLMF:04.09:E', mod_label('\\begin{equation}\label{eq:EF.EX.TM}'))
        self.assertEqual('DLMF:04.09:E', mod_label('\\begin{equation}\\formula{eq:EF.EX.TM}'))
