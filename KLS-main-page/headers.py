file = open("main_page.mmd", "r")
lines = file.read()
listStart = lines.find("= Definition Pages =")
listStart = lines.find("* [[Definition:", listStart)
listEnd = lines.find("</div", listStart)
lines = lines[listStart:listEnd]
lines = lines.split("\n")
pages = []
for x in lines:
    if "Definition:" in x: pages.append(x[x.find("Definition:"):x.find("|")])
mainPage = open("main_page.mmd", "r")
mainLines = mainPage.read()
mainLines = mainLines[mainLines.find("drmf_bof"):mainLines.rfind("drmf_eof\n") + len("drmf_eof\n")]
mainPage.close()
main = open("main_page.mmd", "w")
mainPages = mainLines.split("drmf_eof")
if mainPages[-1].strip() == "":
    mainPages = mainPages[0:len(mainPages) - 1]
x = 0
for g in mainPages:
    if not "\'\'\'Definition:" in g:
        h = g.replace("drmf_eof", "")
        h = g.replace("drmf_bof", "")
        toWrite = "drmf_bof" + h + "drmf_eof\n"
        main.write(toWrite)
    else:
        h = g.replace("drmf_eof", "")
        h = g.replace("drmf_bof", "")
        h = h.strip("\n")
        titleStart = h.find("\'\'\'")
        titleEnd = h.find("\'\'\'", titleStart + len("\'\'\'")) + len("\'\'\'")
        title = h[titleStart:titleEnd]
        h = h[titleEnd:]

        if "<div id=\"drmf_head\">" in h:
            h = h[h.find(">> </div>\n</div>") + len(">> </div>\n</div>"):]
        if "<div id=\"drmf_foot\">" in h:
            h = h[0:h.find("<div id=\"drmf_foot\">")]
        prev = pages[(x - 1) % len(pages)]
        # print h
        next = pages[(x + 1) % len(pages)]
        cur = "Main Page"
        header = "\n<div id=\"drmf_head\">\n"
        header += "<div id=\"alignleft\"> << [[" + prev.replace(" ", "_") + "|" + prev + "]] </div>\n"
        header += "<div id=\"aligncenter\"> [[" + cur.replace(" ", "_") + "|" + cur + "]] </div>\n"
        header += "<div id=\"alignright\"> [[" + next.replace(" ", "_") + "|" + next + "]] >> </div>\n"
        header += "</div>"

        footer = "<div id=\"drmf_foot\">\n"
        footer += "<div id=\"alignleft\"> << [[" + prev.replace(" ", "_") + "|" + prev + "]] </div>\n"
        footer += "<div id=\"aligncenter\"> [[" + cur.replace(" ", "_") + "|" + cur + "]] </div>\n"
        footer += "<div id=\"alignright\"> [[" + next.replace(" ", "_") + "|" + next + "]] >> </div>\n"
        footer += "</div>"
        main.write("drmf_bof\n" + title + header + h + footer + "\ndrmf_eof\n")
        x += 1
