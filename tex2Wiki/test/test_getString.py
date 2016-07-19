
from unittest import TestCase
from tex2Wiki import getString
from tex2Wiki import setup_label_links
class TestGetString(TestCase):

    def test_getString(self):
        self.assertEqual('Mathematical Applications', getString('\\section{Mathematical Applications}\\label{sec:ZE.APPL}%ZE.16\n'))
        self.assertEqual('eq:ZE.INT.EL1',getString('\\eqref{eq:ZE.INT.EL1}'))
        self.assertEqual('eq:ZE.INT.EL3',getString('\\eqref{eq:ZE.INT.EL3}\n'))
        self.assertEqual('eq:ZE.INT.EL5', getString(' \n \\eqref{eq:ZE.INT.EL5}\n '))