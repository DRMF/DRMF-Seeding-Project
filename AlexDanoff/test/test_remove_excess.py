from unittest import TestCase
from remove_excess import remove_section


class TestRemoveExcess(TestCase):
    def test_remove_section(self):
        content = 'AA{Begin} This should be removed {End}DDBB'
        result = remove_section(r'{Begin}', r'{End}', content)
        self.assertEqual('AA{End}DDBB', result)

