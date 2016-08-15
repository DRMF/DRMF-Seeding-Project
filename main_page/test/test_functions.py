#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

from unittest import TestCase
import src.functions as m

update_macro_list_test_cases = [
    {
        "exp": open("main_page/test/macro_list_tests/exp.1.txt").read(),
        "res": (
            open("main_page/test/macro_list_tests/res.1.txt").read(),
            ["* [[Definition:Definition1|Definition1]]", "* [[Definition:Definition2|Definition2]]"]
        )
    }
]

update_headers_test_cases = [
    {
        "exp": open("main_page/test/update_headers_tests/exp.1.txt").read(),
        "def": ["* [[Definition:Definition1|Definition1]]", "* [[Definition:Definition2|Definition2]]",
                "* [[Definition:Definition3|Definition3]]"],
        "res": open("main_page/test/update_headers_tests/res.1.txt").read()
    }
]

add_symbols_data_test_cases = [
    {
        "exp": open("main_page/test/add_symbols_data_tests/exp.1.txt").read(),
        "res": open("main_page/test/add_symbols_data_tests/res.1.txt").read()
    }
]

add_usage_test_cases = [
    {
        "exp": open("main_page/test/add_usage_tests/exp.1.txt").read(),
        "res": open("main_page/test/add_usage_tests/res.1.txt").read()
    }
]


class TestUpdateMacroList(TestCase):
    def test_update_macro_list(self):
        for case in update_macro_list_test_cases:
            self.assertEqual(m.update_macro_list(case["exp"]), case["res"])


class TestUpdateHeaders(TestCase):
    def test_update_headers(self):
        for case in update_headers_test_cases:
            self.assertEqual(m.update_headers(case["exp"], case["def"]), case["res"])


class TestAddSymbolsData(TestCase):
    def test_add_symbols_data(self):
        for case in add_symbols_data_test_cases:
            self.assertEqual(m.add_symbols_data(case["exp"], glossary_location="main_page/test/fake.Glossary.csv"),
                             case["res"])


class TestAddUsage(TestCase):
    def test_add_usage(self):
        for case in add_usage_test_cases:
            self.assertEqual(m.add_usage(case["exp"], glossary_location="main_page/test/fake.Glossary.csv"),
                             case["res"])
