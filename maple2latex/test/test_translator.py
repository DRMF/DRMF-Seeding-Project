#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

import json
from unittest import TestCase
import src.translator as t

TEST_CASES = json.loads(open("test/test_cases.json").read())["translator"]

parse_brackets_test_cases = TEST_CASES["parse_brackets"]
trim_parens_test_cases = TEST_CASES["trim_parens"]
basic_translate_test_cases = TEST_CASES["basic_translate"]
get_arguments_test_cases = TEST_CASES["get_arguments"]
translate_test_cases = TEST_CASES["translate"]
make_equation_test_cases = TEST_CASES["make_equation"]


class TestParseBrackets(TestCase):
    def test_parse_brackets(self):
        for case in parse_brackets_test_cases:
            self.assertEqual(t.parse_brackets(case["exp"]), case["res"])


class TestTrimParens(TestCase):
    def test_trim_parens(self):
        for case in trim_parens_test_cases:
            self.assertEqual(t.trim_parens(case["exp"]), case["res"])


class TestBasicTranslate(TestCase):
    def test_basic_translate(self):
        for case in basic_translate_test_cases:
            self.assertEqual(t.basic_translate(case["exp"]), case["res"])


class TestGetArguments(TestCase):
    def test_get_arguments(self):
        for case in get_arguments_test_cases:
            self.assertEqual(t.get_arguments(case["function"], case["arg_string"]), case["res"])


class TestTranslate(TestCase):
    def test_translate(self):
        for case in translate_test_cases:
            self.assertEqual(t.translate(case["exp"]), case["res"])


class TestMakeEquation(TestCase):
    def test_make_equation(self):
        for case in make_equation_test_cases:
            self.assertEqual(t.make_equation(t.MapleEquation(case["eq"]), case["view_metadata"]), case["res"])
