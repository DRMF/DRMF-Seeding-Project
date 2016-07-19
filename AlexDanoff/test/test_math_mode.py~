import unittest
import mathmode

DELIM_TESTS = [
    {
        "args": ["$test$"],
        "output": "$"
    },
    {
        "args": ["$$test$$"],
        "output": "$$"
    },
    {
        "args": [" \\begin{equation}test\\end{equation}  "],
        "output": "\\begin{equation}"
    },
    {
        "args": ["\\hbox{}", False],
        "output": "\\hbox{"
    }
]

MATH_TESTS = [
    {
        "string": "$\\frac 1 2$ test",
        "start": 0,
        "output": 10
    },
    {
        "string": "\\[2\\hbox{Test}\\]",
        "start": 22,
        "output": 15
    },
    {
        "string": "$\\$$",
        "start": 12,
        "output": 3
    },
    [
        (1, 10),
        (24, 25),
        (13, 15)
    ]
]

NON_MATH_TESTS = [
    {
        "string": "\\mbox{Test\\(test\\)} ",
        "start": 14,
        "output": 19
    },
    {
        "string": "test \\\\(\\begin{align*}\\end{align*}\\\\[",
        "start": 56,
        "output": 37
    },
    {
        "string": "\\begin{multline}\n\\left(2\\right)\n\\end{multline}",
        "start": 3,
        "output": 46
    },
    [
        (26, 30),
        (19, 35)
    ]
]

RANGE_TESTS = [
    {
        "string": "test \\begin{multline*}\ntest \\hbox{Test}\\end{multline*}",
        "output": [
            (22, 28)
        ]
    },
    {
        "string": "$2$ \\begin{align}Test\\end{align}",
        "output": [
            (1, 2),
            (17, 21)
        ]
    },
    {
        "string": "test",
        "output": []
    }
]


class TestMathMode(unittest.TestCase):

    def test_first_delim(self):
        for test in DELIM_TESTS:
            self.assertEqual(mathmode.first_delim(*test["args"]), test["output"])

    def test_parse_math(self):
        ranges = []
        for test in MATH_TESTS[:-1]:
            self.assertEqual(mathmode.parse_math(test["string"], test["start"], ranges), test["output"])
        self.assertEqual(ranges, MATH_TESTS[-1])
        self.assertRaises(SyntaxError, mathmode.parse_math, "\\begin{equation*}", 23, [])

    def test_parse_non_math(self):
        ranges = []
        for test in NON_MATH_TESTS[:-1]:
            self.assertEqual(mathmode.parse_non_math(test["string"], test["start"], ranges), test["output"])
        self.assertEqual(ranges, NON_MATH_TESTS[-1])
        self.assertRaises(SyntaxError, mathmode.parse_non_math, "\\text{", 9, [(1, 4)])

    def test_find_math_ranges(self):
        for test in RANGE_TESTS:
            self.assertEqual(mathmode.find_math_ranges(test["string"]), test["output"])
        self.assertRaises(SyntaxError, mathmode.find_math_ranges("{$$}$$"))

if __name__ == "__main__":
    unittest.main()
