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