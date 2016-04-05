from unittest import TestCase
from parentheses import insert, remove

testCases = [{
    'normal': '\\sin(x)',
    'replaced': '\\sin###open_0###x###close_0###',
}, {
    'normal': '\\sin{x}',
    'replaced': '\\sin{x}',
},
    {
        'normal': '\\sin{x}',
        'replaced': '\\sin###open_0###x###close_0###',
        'curly': True
    }
]

roundTripTests = [{
    'normal': '\\sin(\\arcsin(x))',
}, {
    'normal': '\\sin{\\arcsin(x)}',
}, {
    'normal': '\\sin{\\arcsin(x)}',
    'curly': True
}, {
    'normal': '\\sin{\\arcsin{x}}',
    'curly': True
},
]


class TestInsert(TestCase):
    def test_insert(self):
        for case in testCases:
            self.assertEqual(case['normal'], insert(case['replaced'], case.get('curly', False)))

    def test_remove(self):
        for case in testCases:
            self.assertEqual(case['replaced'], remove(case['normal'], case.get('curly', False)))

    def test_round_trip(self):
        for case in testCases:
            output = insert(remove(case['normal'], case.get('curly', False)), case.get('curly', False))
            self.assertEqual(case['normal'], output)

    def test_extended_round_trip(self):
        for case in roundTripTests:
            output = insert(remove(case['normal'], case.get('curly', False)), case.get('curly', False))
            self.assertEqual(case['normal'], output)
