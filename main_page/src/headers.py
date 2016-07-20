__author__ = "Azeem Mohammed"
__status__ = "Development"

import copy

with open("main_page.mmd", "r") as main_page:
    lines = main_page.read()
    main_lines = copy.copy(lines)

start = lines.find("* [[Definition:", lines.find("= Definition Pages ="))
end = lines.find("</div", start)
lines = lines[start:end].split("\n")

pages = list()

for line in lines:
    if "Definition:" in line:
        pages.append(line[line.find("Definition:"):line.find("|")])

main_lines = main_lines[main_lines.find("drmf_bof"):main_lines.rfind("drmf_eof\n") + len("drmf_eof\n")]
main_pages = main_lines.split("drmf_eof")

if main_pages[-1].strip() == "":
    main_pages = main_pages[0:-1]

count = 0
with open("main_page.mmd", "w") as main_page:
    for page in main_pages:
        # the line below does nothing? (I commented it out)
        # text = page.replace("drmf_eof", "")
        text = page.replace("drmf_bof", "")

        if "'''Definition:" not in page:
            main_page.write("drmf_bof" + text + "drmf_eof\n")

        else:
            text = text.strip("\n")
            title_start = text.find("'''")
            title_end = text.find("'''", title_start + len("'''")) + len("'''")
            title = text[title_start:title_end]
            text = text[title_end:]

            if "<div id=\"drmf_head\">" in text:
                search_string = ">> </div>\n</div>"
                text = text[text.find(search_string) + len(search_string):]

            if "<div id=\"drmf_foot\">" in text:
                text = text[:text.find("<div id=\"drmf_foot\">")]

            prev = pages[(count - 1) % len(pages)]
            cur = "Main Page"
            next = pages[(count + 1) % len(pages)]

            delimiter = "\n<div id=\"alignleft\"> << [[" + prev.replace(" ", "_") + "|" + prev + "]] </div>" + \
                        "\n<div id=\"aligncenter\"> [[" + cur.replace(" ", "_") + "|" + cur + "]] </div>" + \
                        "\n<div id=\"alignright\"> [[" + next.replace(" ", "_") + "|" + next + "]] >> </div>" + \
                        "\n</div>"

            header = "\n<div id=\"drmf_head\">" + delimiter
            footer = "<div id=\"drmf_foot\">" + delimiter

            main_page.write("drmf_bof\n" + title + header + text + footer + "\ndrmf_eof\n")

            count += 1
