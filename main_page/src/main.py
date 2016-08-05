__author__ = "Azeem Mohammed"
__status__ = "Development"
__credits__ = ["Joon Bang", "Azeem Mohammed"]

import time
import symbols_list
import mod_main

"""
Order:
- List
- Symbols List
- Headers
- List Ways
"""


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


def main():
    if raw_input("Update main page? (y/n): ") == "n":
        return

    # read contents
    with open("main_page.mmd") as main_page:
        text = main_page.read()

        # create backup
        local_time = time.asctime(time.localtime(time.time())).split()
        local_time = "_" + '_'.join(local_time[1:3] + local_time[3:][::-1])
        with open("backups/main_page" + local_time + ".mmd.bak", "w") as backup:
            backup.write(text)

    text, definitions = update_macro_list(text)
    text = symbols_list.main(text)
    text = update_headers(text, definitions)
    text = mod_main.main(text)

    with open("main_page.mmd", "w") as main_page:
        main_page.write(text)


if __name__ == '__main__':
    main()
