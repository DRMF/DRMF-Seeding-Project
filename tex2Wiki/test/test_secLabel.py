from unittest import TestCase
from tex2Wiki import secLabel
from tex2Wiki import setup_label_links
class TestSecLabel(TestCase):
    def test_secLabel(self):
        self.assertEqual('Formula:DLMF:25.5:E12',secLabel("Formula:DLMF:25.5:E12''"))