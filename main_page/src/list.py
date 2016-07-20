__author__ = "Azeem Mohammed"
__status__ = "Development"

import copy
import time


def compare_string(a, b):
    """Returns whether string a is "less than" string b, up to the pipe symbol."""
    x = a[:a.find("|")]
    y = b[:b.find("|")]

    # pipe missing in a string
    if not x or not y:
        return True

    return x < y


def sum_ordinal(string):
    """Returns the sum of the ordinal values of all characters in string."""
    return sum((ord(ch) for ch in string))


def sort(strings):
    return sorted(copy.deepcopy(strings), cmp=compare_string)


def main():
    localtime = time.asctime(time.localtime(time.time())).replace(" ", "_")
    with open("main_page.mmd") as main_page:
        with open("backups/main_page.mmd" + str(localtime), "w") as main_page_bak:
            main_page_bak.write(main_page.read())

    with open("main_page.mmd") as main_page:
        main_text = main_page.read()

    main_lines = main_text.split("\n")

    text = ""

    for line in main_lines:
        if "'''Definition:" in line:
            definition = line[line.find("'''Definition:") + 3:line.find("'''", line.find("'''Definition:") + 4)]
            element = "* [[" + definition + "|" + definition[len("Definition:"):] + "]]"
            text += element + "\n"

    s = main_text.find("== Definition Pages ==")
    e = main_text.find("= Copyright =")

    text = main_text[:s] + \
           "== Definition Pages ==\n\n<div style=\"-moz-column-count:2; column-count:2;-webkit-column-count:2\">\n" + \
           text + "</div>\n\n" + main_text[e:]

    with open("main_page.mmd", "w") as main_page:
        main_page.write(text)

if __name__ == '__main__':
    main()