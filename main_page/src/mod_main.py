__author__ = "Azeem Mohammed"
__status__ = "Development"

import copy
import csv

DEF_STRING = "'''Definition:"


def at_sort(strings):
    """Sorts by number of @ symbols in string."""

    return sorted(copy.copy(strings), key=lambda ch: ch.count("@"))


def remove_brackets_text(string):
    left_brackets = 0
    text = ""

    for ch in string:
        if ch == "[":
            left_brackets += 1
        elif ch == "]":
            left_brackets -= 1
        elif not left_brackets:
            text += ch

    return text


def find_all_pos(info):
    # TODO: what is info? what does pos mean???

    original = info[0]
    key_string = info[3]

    before, key_string = key_string.split("|", 1)
    keys = key_string.split(":")
    ret = []

    for key in keys:
        if key in ["F", "FO", "O", "O1"]:
            if "@" in original:
                ret.append(original[:original.find("@")])
                if key == "O":
                    ret.append(original)
            else:
                ret.append(original)
        elif key == "FnO":  # remove optional parameters
            if original.find("@") != -1:
                ret.append(remove_brackets_text(original[0:original.find("@")]))
            else:
                ret.append(remove_brackets_text(original))
        elif key in ["P", "PO"]:
            ret.append(original.replace("@@", "@"))
        elif key == "PnO":  # remove optional parameters
            ret.append(remove_brackets_text(original.replace("@@", "@")))
        elif key in ["nP", "nPO", "PS", "O2"]:
            ret.append(original)
        elif key == "nPnO":  # remove optional paramters
            ret.append(remove_brackets_text(original))

        if "fo" in key:
            ret.append(original.replace("@@@", "@" * int(key[2])))

    return at_sort(ret), before

with open("main_page.mmd") as main_page:
    lines = main_page.read()

lines = lines.replace("The LaTeX DLMF macro '''\\", "The LaTeX DLMF and DRMF macro '''\\")

with open("Categories.txt") as categories:
    cats = [category.strip() for category in categories.readlines()]

text = ""
i = 0

while True:
    n = lines.find(DEF_STRING, i)
    if n == -1:
        break
    else:
        macroN = lines[n + len(DEF_STRING):lines.find("'''", n + len(DEF_STRING))]
        r = lines.find("'''\\", n)
        q = lines.find("'''", r + len("'''\\"))

        if lines[r:q].find("{") != -1:
            lines = lines[:r] + "'''\\" + macroN + lines[q:]

        if lines.find("\nThis macro is in the category of", n) < lines.find(DEF_STRING, n + 15) \
                and "\nThis macro is in the category of" in lines[n:]:
            p = lines.find("\nThis macro is in the category of", n)
        else:
            p = lines.find("\n", lines.find(".", n))

        text += lines[i:p].rstrip() + "\n\n"

        count = 0
        list_calls = []

        glossary = csv.reader(open('new.Glossary.csv', 'rb'), delimiter=',', quotechar='\"')
        for entry in glossary:
            if not entry[0].find("\\" + macroN) and (len(entry[0]) == len(macroN) + 1 or not entry[0][len(macroN) + 1].isalpha()):
                q, s = find_all_pos(entry)
                list_calls += q
                count += len(q)

        for cat in cats:
            if s + "    -" in cat:
                category = "This macro is in the category of" + cat[cat.find("-") + 2:] + "\n\n"
                break

        new = category + "In math mode, this macro can be called in the following way" + "s" * (count > 1) + ":\n\n"

        for q in range(0, len(list_calls)):
            c = list_calls[q]
            new += ":'''" + c + "'''" + " produces <math>{\\displaystyle " + c + "}</math><br />\n"

        # Now add the multiple ways \macroname{n}@... produces <math>\macroname{n}@...</math>
        text += new + "\n"
        i = lines.find("These are defined by", p)

with open("main_page.mmd", "w") as main_page:
    main_page.write(text + lines[i:])
