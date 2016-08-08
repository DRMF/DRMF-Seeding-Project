__author__ = "Azeem Mohammed"
__status__ = "Development"
__credits__ = ["Joon Bang", "Azeem Mohammed"]

import csv
import time
import mod_main

GLOSSARY_LOCATION = "new.Glossary.csv"


def generate_html(tag_name, options, text, spacing=True):
    result = "<" + tag_name
    if options != "":
        result += " " + options
    result += ">\n" + text + "\n</" + tag_name + ">\n"

    if not spacing:
        return result.replace("\n", " ")[:-1] + "\n"

    return result


def update_macro_list(text):
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


def get_macro_name(macro):
    macro_name = ""
    for ch in macro:
        if ch.isalpha():
            macro_name += ch
        elif ch in ["@", "{", "["]:
            break

    return macro_name


def get_symbols(text, glossary):
    symbols = list()
    for keyword in list(glossary):
        for space in ["{", "@", "[", "\\", " "]:
            if "\\" + keyword + space in text:
                symbols.append(keyword)

    span_text = ""
    for symbol in set(sorted(symbols)):
        t = ""
        link = glossary[symbol][-2]
        meaning = list(glossary[symbol][1])

        count = 0
        for i, ch in enumerate(meaning):
            if ch == "$" and count % 2 == 0:
                meaning[i] = "<math{\\displaystyle "
                count += 1
            elif ch == "$":
                meaning[i] = "</math>"
                count += 1

        appearance = glossary[symbol][4].strip("$")

        span_text += "<span class=\"plainlinks\">[" + link + " <math>{\\displaystyle " + appearance + \
                     "}</math>]</span> : " + ''.join(meaning) + " : [" + link + " " + link + "]<br />\n"

    return span_text[:-1]


def add_symbols_data(data):
    glossary = dict()
    with open(GLOSSARY_LOCATION, "rb") as csv_file:
        glossary_file = csv.reader(csv_file, delimiter=',', quotechar='\"')
        for row in glossary_file:
            glossary[get_macro_name(row[0])] = row

    pages = data[data.find("drmf_bof"):].split("drmf_eof")[:-1]

    print "Pages: " + str(len(pages))

    result = ""
    for page in pages:
        # skip over non-definition pages
        if "'''Definition:" not in page:
            to_write = page + "drmf_eof\n"
            result += to_write
            continue

        page = page.replace("drmf_bof", "").strip("\n")
        add_spacing = False
        sflag2 = False
        # remove data (to be regenerated later)
        if page.find("== Symbols List ==") != -1:
            to_write = page.split("== Symbols List ==")[0]
            page = to_write
        else:
            add_spacing = True
            if page.find("drmf_foot") == -1:
                to_write = page
                sflag2 = True
            else:
                to_write = page.split("<div id=\"drmf_foot\">")[0]
                page = to_write

        to_write = "drmf_bof\n" + to_write
        if add_spacing:
            to_write += "\n\n"

        to_write += "== Symbols List ==\n\n"
        to_parse = page.split("defined by")[1].split("<br />")[0]
        to_write += get_symbols(to_parse, glossary)
        to_write += "\n<br />\ndrmf_eof\n\n"
        if sflag2:
            to_write += "\n"
        result += to_write

    return result


def create_backup():
    with open("main_page.mmd") as current:
        local_time = time.asctime(time.localtime(time.time())).split()
        local_time = "_" + '_'.join(local_time[1:3] + local_time[3:][::-1])
        with open("backups/main_page" + local_time + ".mmd.bak", "w") as backup:
            backup.write(current.read())


def main():
    if raw_input("Update main page? (y/n): ") == "n":
        return

    # read contents
    with open("main_page.mmd") as main_page:
        text = main_page.read()

    text, definitions = update_macro_list(text)
    text = add_symbols_data(text)
    text = update_headers(text, definitions)
    text = mod_main.main(text)

    # only create backup if program did not crash
    # create_backup()

    with open("main_page.mmd", "w") as main_page:
        main_page.write(text)


if __name__ == '__main__':
    main()
