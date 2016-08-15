__author__ = "Joon Bang"
__status__ = "Development"

import csv

GLOSSARY_LOCATION = "main_page/new.Glossary.csv"


def generate_html(tag_name, options, text, spacing=True):
    # (str, str, str(, bool)) -> str
    """Generates an html tag, with optional html parameters."""
    result = "<" + tag_name
    if options != "":
        result += " " + options
    result += ">\n" + text + "\n</" + tag_name + ">\n"

    if not spacing:
        return result.replace("\n", " ")[:-1] + "\n"

    return result


def get_macro_name(macro):
    # (str) -> str
    """Obtains the macro name."""
    macro_name = ""
    for ch in macro:
        if ch.isalpha() or ch == "\\":
            macro_name += ch
        elif ch in ["@", "{", "["]:
            break

    return macro_name


def find_all(pattern, string):
    # (str, str) -> generator
    """Finds all instances of pattern in string."""

    i = string.find(pattern)
    while i != -1:
        yield i
        i = string.find(pattern, i + 1)


def remove_optional_params(string):
    # (str) -> str
    """Removes optional parameters from a LaTeX semantic macro."""
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


def get_all_variants(entry):
    # (str) -> str
    """Returns string containing info on all variants of a macro."""
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
    # (str, str) -> bool
    """Determines whether the entry refers to the macro."""
    return macro in entry and (len(macro) == len(entry) or not entry[len(macro)].isalpha())


def update_macro_list(text):
    # (str) -> str
    """Updates the list of macros found in the main page of main_page.mmd."""
    lines = text.split("\n")
    definitions = list()

    for line in lines:
        if "'''Definition:" in line:
            macro = line.split("'''")[1][11:]
            element = "* [[Definition:" + macro + "|" + macro + "]]"
            definitions.append(element)

    def_contents = generate_html("div", "style=\"-moz-column-count:2; column-count:2;-webkit-column-count:2\"",
                                 "\n".join(definitions))

    start = text.find("== Definition Pages ==")
    end = text.find("= Copyright =")

    return text[:start + 23] + "\n" + def_contents + "\n" + text[end:], definitions


def update_headers(text, definitions):
    # (str, list) -> str
    """Updates the headers used for navigation for every page."""
    pages = text.split("drmf_eof")[:-1]

    macros = list()
    formatted = list()
    for definition in definitions:
        macros.append("Definition:" + definition.split("|")[1][:-2])
        formatted.append("[[" + macros[-1].replace(" ", "_") + "|" + macros[-1] + "]]")

    output = ""

    i = 0
    for page in pages:
        if "'''Definition:" not in page:
            output += page + "drmf_eof\n"
            continue

        # remove drmf_bof and definition header to prevent redundancy
        page = page[page.find(macros[i]) + len(macros[i]) + 3:]

        if "<div id=\"drmf_head\">" in page:
            page = page[page.find(">> </div>\n</div>") + len(">> </div>\n</div>"):]

        if "<div id=\"drmf_foot\">" in page:
            page = page[:page.find("<div id=\"drmf_foot\">")]

        nav_section = generate_html("div", "id=\"alignleft\"", "<< " + formatted[i - 1], spacing=False) + \
                      generate_html("div", "id=\"aligncenter\"", "[[Main_Page|Main Page]]", spacing=False) + \
                      generate_html("div", "id=\"alignright\"", formatted[(i + 1) % len(formatted)] + " >>",
                                     spacing=False)[:-1]

        header = generate_html("div", "id=\"drmf_head\"", nav_section)[:-1]
        footer = generate_html("div", "id=\"drmf_foot\"", nav_section)[:-1]

        output += "drmf_bof\n" + "'''" + macros[i] + "'''\n" + header + page[:-1] + footer + "\ndrmf_eof\n"

        i += 1

    return output


def get_symbols(text, glossary):
    # (str, dict) -> str
    """Generates span text based on symbols present in text."""
    symbols = set()

    for keyword in glossary:
        for index in find_all(keyword, text):
            # if the macro is present in the text
            if index != -1:
                index += len(keyword)  # now index of next character

                if index >= len(text) or not text[index].isalpha():
                    symbols.add(keyword)

    span_text = ""
    for symbol in sorted(symbols, key=str.lower):
        links = list()
        for cell in glossary[symbol]:
            if "http://" in cell or "https://" in cell:
                links.append(cell)

        id_link = links[0]
        links = ["[" + link + " " + link + "]" for link in links]

        meaning = list(glossary[symbol][1])

        count = 0
        for i, ch in enumerate(meaning):
            if ch == "$" and count % 2 == 0:
                meaning[i] = "<math>{\\displaystyle "
                count += 1
            elif ch == "$":
                meaning[i] = "}</math>"
                count += 1

        appearance = glossary[symbol][4].strip("$")

        span_text += "<span class=\"plainlinks\">[" + id_link + " <math>{\\displaystyle " + appearance + \
                     "}</math>]</span> : " + ''.join(meaning) + " : " + " ".join(links) + "<br />\n"

    return span_text[:-7]  # slice off the extra br and endline


def add_symbols_data(data, glossary_location=GLOSSARY_LOCATION):
    # (str(, str)) -> str
    """Adds list of symbols present in page under symbols list section."""
    glossary = dict()
    with open(glossary_location, "rb") as csv_file:
        glossary_file = csv.reader(csv_file, delimiter=',', quotechar='\"')
        for row in glossary_file:
            glossary[get_macro_name(row[0])] = row

    pages = data[data.find("drmf_bof"):].split("drmf_eof")[:-1]

    result = ""
    for page in pages:
        # skip over non-definition pages
        if "'''Definition:" not in page:
            result += page + "drmf_eof\n"
            continue

        page = page.replace("drmf_bof", "").strip("\n")
        add_spacing = False
        # remove data (to be regenerated later)
        if "== Symbols List ==" in page:
            to_write = page.split("== Symbols List ==")[0]
            page = to_write
        else:
            add_spacing = True
            if page.find("drmf_foot") == -1:
                to_write = page
            else:
                to_write = page.split("<div id=\"drmf_foot\">")[0].rstrip("\n")
                page = to_write

        to_write = "drmf_bof\n" + to_write
        if add_spacing:
            to_write += "\n\n"

        to_write += "== Symbols List ==\n\n"
        to_write += get_symbols(page, glossary)
        to_write += "\n<br />\ndrmf_eof\n"
        result += to_write

    return result


def add_usage(lines, glossary_location=GLOSSARY_LOCATION):
    # (str(, str)) -> str
    """Adds the macro category information and calling sequences."""
    with open("main_page/categories.txt") as cats:
        categories = cats.readlines()

    to_write = ""
    i = 0

    while True:
        n = lines.find("'''Definition:", i)
        if n == -1:
            break

        macro_name = lines[n:].split("'''")[1][11:]
        left = lines.find("'''\\", n)
        right = lines.find("'''", left + len("'''\\"))

        if lines[left:right].find("{") != -1:
            lines = lines[:left] + "'''\\" + macro_name + lines[right:]

        if lines.find("\nThis macro is in the category of", n) < lines.find("'''Definition:", n + len(
                "'''Definition:") + 1) and lines.find("\nThis macro is in the category of", n) != -1:
            p = lines.find("\nThis macro is in the category of", n)
        else:
            p = lines.find(".\n", n) + 1

        to_write += lines[i:p].rstrip() + "\n\n"

        calls = []
        glossary = csv.reader(open(glossary_location, 'rb'), delimiter=',', quotechar='\"')
        for entry in glossary:
            if macro_match("\\" + macro_name, entry[0]):
                macro_calls, category = get_all_variants(entry)
                calls += macro_calls

        for line in categories:
            key, meaning = line.split(" - ")
            if key == category:
                category_text = "This macro is in the category of " + meaning
                break
        else:
            category_text = "This macro is in the category of integer valued functions.\n"

        text = category_text + "\nIn math mode, this macro can be called in the following way" + "s" * (
            len(calls) > 1) + ":\n\n"

        for call in calls:
            text += ":'''" + call + "'''" + " produces <math>{\\displaystyle " + call + "}</math><br />\n"

        # Now add the multiple ways \macroname{n}@... produces <math>\macroname{n}@...</math>
        print text
        to_write += text + "\n"
        i = lines.find("These are defined by", p)

    return to_write + lines[i:]
