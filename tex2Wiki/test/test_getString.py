
from unittest import TestCase
from tex2Wiki import get_string
from tex2Wiki import setup_label_links
class TestGetString(TestCase):

    def test_getString(self):
        self.assertEqual('Mathematical Applications', get_string('\\section{Mathematical Applications}\\label{sec:ZE.APPL}%ZE.16\n'))
        self.assertEqual('eq:ZE.INT.EL1', get_string('\\eqref{eq:ZE.INT.EL1}'))
        self.assertEqual('eq:ZE.INT.EL3', get_string('\\eqref{eq:ZE.INT.EL3}\n'))
        self.assertEqual('eq:ZE.INT.EL5', get_string(' \n \\eqref{eq:ZE.INT.EL5}\n '))