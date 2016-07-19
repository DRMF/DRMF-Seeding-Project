math_start = {"\\[": "\\]",
              "\\(": "\\)",
              "$$": "$$",
              "$": "$",
              "\\begin{equation}": "\\end{equation}",
              "\\begin{equation*}": "\\end{equation*}",
              "\\begin{align}": "\\end{align}",
              "\\begin{align*}": "\\end{align*}",
              "\\begin{multline}": "\\end{multline}",
              "\\begin{multline*}": "\\end{multline*}"}

math_end = ["\\hbox{",
            "\\mbox{",
            "\\text{"]


def find_first(string, delim, start=0):
    # type: (str, str, int) -> int
    """
    Finds the first occurrence of a delimiter within a string.
    :param string: The string to search within.
    :param delim: The delimiter to search for.
    :param start: The starting index in the string.
    :return: The index of the first occurrence.
    """
    i = string.find(delim, start)
    if delim in ["$", "\\[", "\\("]:
        if i == -1:
            return -1
        elif i != 0 and string[i - 1] == "\\":
            return find_first(string, delim, i + len(delim))
    return i


def first_delim(string, enter=True):
    # type: (str, bool) -> str
    """
    Finds the first math or text mode delimiter within a string.
    :param string: The string to search within.
    :param enter: Whether to find a math mode or a text mode delimiter.
    :return: The delimiter that first appears in the string.
    """
    minm = ["\\hbox{", "\\]"][enter]
    for delim in [math_end, math_start][enter]:
        i = find_first(string, delim)
        if i != -1 and i < find_first(string, minm) or minm not in string:
            minm = delim
    if minm == "$" and string.find("$$") == string.find("$"):
        minm = "$$"
    return minm


def does_exit(string):
    # type: (str) -> bool
    """
    Returns whether a string starts with a text mode delimiter.
    :param string: The string to check.
    :return: Whether the string starts with a text mode delimiter.
    """
    return any(string.startswith(delim) for delim in math_end)


def does_enter(string):
    # type: (str) -> bool
    """
    Returns whether a string starts with a math mode delimiter.
    :param string: The string to check.
    :return: Whether the string starts with a math mode delimiter.
    """
    return any(string.startswith(delim) for delim in math_start)


def parse_math(string, start, ranges):
    # type: (str) -> str, int
    """
    Finds the ranges of the current math mode segment.
    :param string: The string to parse.
    :param start: The starting index in the original string.
    :param ranges: The ranges of all math mode segments.
    :return i: The length of the math mode segment.
    """
    delim = first_delim(string)
    i = len(delim)
    begin = start + i
    while i < len(string):
        if string[i:].startswith("\\$"):
            i += 1
        elif string[i:].startswith("\\\\]"):
            i += 2
        elif string[i:].startswith("\\\\)"):
            i += 2
        else:
            if does_exit(string[i:]):
                if begin != start + i:
                    ranges.append((begin, start + i))
                i += parse_non_math(string[i:], start + i, ranges)
                begin = start + i
            if string[i:].startswith(math_start[delim]):
                if begin != start + i:
                    ranges.append((begin, start + i))
                return i + len(math_start[delim]) - 1
        i += 1
    return i


def parse_non_math(string, start, ranges):
    # type: (str) -> str, int
    """
    Finds occurrences of math mode within a segment of text mode.
    :param string: The string to parse.
    :param start: The starting index in the original string.
    :param ranges: The ranges of all math mode segments.
    :return i: The length of the text mode segment.
    """
    delim = first_delim(string, False)
    if not string.startswith(delim):
        delim = ""
    level = 0
    i = len(delim)
    while i < len(string):
        if string[i:].startswith("\\$"):
            i += 1
        elif string[i:].startswith("\\\\["):
            i += 2
        elif string[i:].startswith("\\\\("):
            i += 2
        elif does_enter(string[i:]):
            i += parse_math(string[i:], start + i, ranges)
        elif string[i] == "{":
            level += 1
        elif string[i] == "}":
            if level == 0 and delim != "":
                i += 1
                return i
            else:
                level -= 1
        i += 1
    return i


def find_math_ranges(string, drmf):
    # type: (str) -> list
    """
    Returns a list of tuples, each tuple denoting a range of math mode.
    :param string: The string to search within.
    :return: A list of tuples denoting math mode ranges.
    """
    global math_end
    if drmf:
        string = string.replace("\\drmfnote", "\\drmfname")
        math_end.extend(["\\constraint{",
                         "\\substitution"
                         "\\drmfnote{",
                         "\\drmfname{",
                         "\\proof{",
                         "\\label{"])
    ranges = []
    parse_non_math(string, 0, ranges)
    return ranges[:]
