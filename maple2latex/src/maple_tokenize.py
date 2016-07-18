#!/usr/bin/env python

__author__ = "Joon Bang"
__status__ = "Development"

symbols = [
    "+",
    "-",
    "*",
    "/",
    "^",
    "!",
    "=",
    "<",
    ">",
    "@",
    "$",
    ",",
    "~",
    "(",
    ")",
    "{",
    "}",
    "\'",
    "\"",
    "|",
    "&",
    "_",
    "%",
    "\\",
    "#",
    "?"
]


def tokenize(string):
    for symbol in symbols:
        string = string.replace(symbol, " " + symbol + " ")

    return string.split()