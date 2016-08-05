__author__ = "Azeem Mohammed"
__status__ = "Development"
__credits__ = ["Joon Bang", "Azeem Mohammed"]

import csv

GLOSSARY_LOCATION = "new.Glossary.csv"


def remove_optional_params(string):
    parse = True
    text = ""
    for ch in string:
        if parse and ch == "[":
            parse = False
        elif parse:
            text += ch
        else:
            if ch == "]":
                parse = True

    return text


def find_all_positions(entry):
    macro = entry[0]
    category = entry[3].split("|", 1)[0]
    keys = entry[3].split("|", 1)[1].split(":")
    result = []

    for key in keys:
        if key in ["F", "FO", "O", "O1"]:
            result.append(macro.split("@", 1)[0])
            if macro.count("@") > 0 and key == "O":
                result.append(macro)

        if key == "FnO":  # remove optional parameters
            string = macro
            if macro.count("@") > 0:
                string = string[:string.find("@")]
            result.append(remove_optional_params(string))

        if key in ["P", "PO", "PnO"]:
            result.append(macro.replace("@@", "@"))

        if key == "PnO":  # remove optional parameters
            result[-1] = remove_optional_params(result[-1])

        if key in ["nP", "nPO", "PS", "O2"]:
            result.append(macro)

        if key == "nPnO":  # remove optional paramters
            result.append(remove_optional_params(macro))

        if "fo" in key:
            result.append(macro.replace("@@@", "@" * int(key[2])))

    return sorted(result, key=lambda x: x.count("@")), category


def macro_match(macro, entry):
    """Determines whether the entry refers to the macro."""
    return macro in entry and (len(macro) == len(entry) or not entry[len(macro)].isalpha())


def main(lines):
    lines = lines.replace("The LaTeX DLMF macro '''\\", "The LaTeX DLMF and DRMF macro '''\\")
    to_write = ""
    i = 0

    with open("categories.txt") as cats:
        categories = cats.readlines()

    while True:
        n = lines.find("'''Definition:", i)
        if n == -1:
            break

        macro_name = lines[n + len("'''Definition:"):lines.find("'''", n + len("'''Definition:"))]
        r = lines.find("'''\\", n)
        q = lines.find("'''", r + len("'''\\"))
        if lines[r:q].find("{") != -1:
            lines = lines[0:r] + "'''\\" + macro_name + lines[q:]

        if lines.find("\nThis macro is in the category of", n) < lines.find("'''Definition:", n + len(
                "'''Definition:") + 1) and lines.find("\nThis macro is in the category of", n) != -1:
            p = lines.find("\nThis macro is in the category of", n)
        else:
            p = lines.find(".\n", n) + 1
        to_write += lines[i:p].rstrip() + "\n\n"

        calls = []
        glossary = csv.reader(open(GLOSSARY_LOCATION, 'rb'), delimiter=',', quotechar='\"')
        for entry in glossary:
            if macro_match("\\" + macro_name, entry[0]):
                macro_calls, category = find_all_positions(entry)
                calls += macro_calls

        for line in categories:
            key, meaning = line.split(" - ")
            if key == category:
                category_text = "This macro is in the category of " + meaning
                break

        text = category_text + "\nIn math mode, this macro can be called in the following way" + "s" * (
            len(calls) > 1) + ":\n\n"

        for call in calls:
            text += ":'''" + call + "'''" + " produces <math>{\\displaystyle " + call + "}</math><br />\n"

        # Now add the multiple ways \macroname{n}@... produces <math>\macroname{n}@...</math>
        to_write += text + "\n"
        i = lines.find("These are defined by", p)

    return to_write + lines[i:]
