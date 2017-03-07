from unittest import TestCase
from tex2Wiki import unmodLabel
from tex2Wiki import setup_label_links
class TestModLabel(TestCase):

    def test_unmodLabel(self):
        self.assertEqual('Formula:DLMF:15.2:E1', unmodLabel('Formula:DLMF:15.02:E1')) #remove 0's before decimal point
        self.assertEqual('Formula:DLMF:5.2:E1', unmodLabel('Formula:DLMF:05.02:E1')) #remove 0's before both decimal points and after colon
