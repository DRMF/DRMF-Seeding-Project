from unittest import TestCase
from parentheses import insert, remove

test_cases = [{
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

round_trip_tests = [{
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
        for case in test_cases:
            self.assertEqual(case['normal'], insert(case['replaced'], case.get('curly', False)))

    def test_remove(self):
        for case in test_cases:
            self.assertEqual(case['replaced'], remove(case['normal'], case.get('curly', False)))

    def test_round_trip(self):
        for case in test_cases:
            output = insert(remove(case['normal'], case.get('curly', False)), case.get('curly', False))
            self.assertEqual(case['normal'], output)

    def test_extended_round_trip(self):
        for case in round_trip_tests:
            output = insert(remove(case['normal'], case.get('curly', False)), case.get('curly', False))
            self.assertEqual(case['normal'], output)
