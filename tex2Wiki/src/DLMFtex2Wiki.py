__author__ = "Azeem Mohammed"
__status__ = "Development"

# Version 15: Minor Fixes
# Convert tex to wikiText
import csv  # imported for using csv format
import sys  # imported for getting args
from shutil import copyfile
from tex2Wiki import append_text, append_revision, get_string_within_, getSym, getEq, secLabel, getEqP, unmodLabel, isnumber


def mod_label(label):
    is_numeric = False
    new_label = ""
    num = ""
    for i in range(len(label)):
        if is_numeric and not isnumber(label[i]):
            if len(num) > 1:
                new_label += num
                num = ""
            else:
                new_label += "0" + str(num)
                num = ""
        if isnumber(label[i]):
            is_numeric = True
            num += str(label[i])
        else:
            is_numeric = False
            new_label += label[i]
    if len(num) > 1:
        new_label += num
    elif len(num) == 1:
        new_label += "0" + num
    return new_label


def dlmf(of_name, mmd, llinks, n):
    for iterations in range(0, 1):
        tex = open(of_name, 'r')
        main_file = open(mmd, "r")
        l_links = open(llinks, 'r')
        main_prepend = ""
        main_write = open("ZetaFunctions.mmd.new", "w")
        l_link_list = l_links.readlines()
        math = False
        constraint = False
        substitution = False
        symbols = []
        lines = tex.readlines()
        ref_lines = []
        sections = []
        labels = []
        eqs = []
        ref_eqs = []
        parse = False
        head = False
        try:
            chap_ref = [("GA", open("../../data/GA.tex", 'r')),
                        ("ZE", open("../../data/ZE.3.tex", 'r'))]
        except IOError:
            chap_ref = [("GA", open("GA.tex", 'r')), ("ZE", open("ZE.3.tex", 'r'))]
        ref_labels = []
        for chap in chap_ref:
            ref_lines = ref_lines + (chap[1].readlines())
            chap[1].close()
        for i in range(len(ref_lines)):
            line = ref_lines[i]
            if "\\begin{equation}" in line:
                s_label = line.find("\\label{") + 7
                e_label = line.find("}", s_label)
                label = line[s_label:e_label]
                for l_link in l_link_list:
                    if l_link.find(label) != -1 and l_link[len(label) + 1] == "=":
                        r_label = l_link[l_link.find("=>") + 3:l_link.find("\\n")]
                        r_label = r_label.replace("/", "")
                        r_label = r_label.replace("#", ":")
                        break
                label = r_label
                ref_labels.append(label)
                ref_eqs.append("")
                math = True
            elif math:
                ref_eqs[-1] += line
                if any([item in ref_lines[i + 1]
                        for item in ["\\end{equation}", "\\constraint", "\\substitution", "\\drmfn"]]):
                    math = False

        start_flag = True
        for i in range(len(lines)):
            line = lines[i]
            if "\\begin{document}" in line:
                parse = True
            elif "\\end{document}" in line:
                main_prepend += "</div>\n"
                main_text = main_prepend
                main_text = main_text.replace("drmf_bof\n", "")
                main_text = main_text.replace("drmf_eof\n", "")
                main_text = main_text.replace(
                    "\'\'\'Zeta and Related Functions\'\'\'\n", "")
                main_text = main_text.replace("{{#set:Section=0}}\n", "")
                append_revision('Zeta and Related Functions')
                main_text = "{{#set:Section=0}}\n" + main_text
                main_write.write(main_text)
                main_write.close()
                main_file.close()
                copyfile(mmd, 'ZetaFunctions.mmd.new')
                parse = False
            elif "\\title" in line and parse:
                labels.append("Zeta and Related Functions")
                sections.append(["Zeta and Related Functions", 0])
            elif "\\part" in line:
                if getString(line) == "BOF":
                    parse = False
                elif getString(line) == "EOF":
                    parse = True
                elif parse:
                    stringWrite = "\'\'\'"
                    stringWrite += getString(line) + "\'\'\'\n"
                    chapter = getString(line)
                    if start_flag:
                        main_prepend += (
                            "\n== Sections in " +
                            chapter +
                            " ==\n\n<div style=\"-moz-column-count:2; column-count:2;-webkit-column-count:2\">\n")
                        start_flag = False
                    else:
                        main_prepend += ("</div>\n\n== Sections in " +
                                         chapter +
                                         " ==\n\n<div style=\"-moz-column-count:2; "
                                         "column-count:2;-webkit-column-count:2\">\n")
                    head = True
            elif "\\section" in line:
                main_prepend += ("* [[" +
                                 secLabel(getString(line)) +
                                 "|" +
                                 getString(line) +
                                 "]]\n")
                sections.append([getString(line)])

        secCounter = 0
        eqCounter = 0
        for i in range(0, len(lines)):
            line = lines[i]
            if "\\section" in line:
                parse = True
                secCounter += 1
                append_revision(secLabel(getString(line)))
                append_text(
                    "{{DISPLAYTITLE:" + (sections[secCounter][0]) + "}}\n")
                append_text("<div id=\"drmf_head\">\n")
                append_text(
                    "<div id=\"alignleft\"> << [[" +
                    secLabel(
                        sections[
                            secCounter -
                            1][0]) +
                    "|" +
                    secLabel(
                        sections[
                            secCounter -
                            1][0]) +
                    "]] </div>\n")
                append_text(
                    "<div id=\"aligncenter\"> [[Zeta_and_Related_Functions#" +
                    "Sections_in_" +
                    chapter.replace(
                        " ",
                        "_") +
                    "|" +
                    secLabel(
                        sections[secCounter][0]) +
                    "]] </div>\n")
                append_text(
                    "<div id=\"alignright\"> [[" +
                    secLabel(
                        sections[
                            (secCounter +
                             1) %
                            len(sections)][0]) +
                    "|" +
                    secLabel(
                        sections[
                            (secCounter +
                             1) %
                            len(sections)][0]) +
                    "]] >> </div>\n</div>\n\n")
                head = True
                append_text("== " + getString(line) + " ==\n")
            elif ("\\section" in lines[(i + 1) % len(lines)] or "\\end{document}" in lines[
                    (i + 1) % len(lines)]) and parse:
                append_text("<div id=\"drmf_foot\">\n")
                append_text(
                    "<div id=\"alignleft\"> << [[" +
                    secLabel(
                        sections[
                            secCounter -
                            1][0]) +
                    "|" +
                    secLabel(
                        sections[
                            secCounter -
                            1][0]) +
                    "]] </div>\n")
                append_text(
                    "<div id=\"aligncenter\"> [[Zeta_and_Related_Functions#" +
                    "Sections_in_"
                    "" +
                    chapter.replace(
                        " ",
                        "_") +
                    "|" +
                    secLabel(
                        sections[secCounter][0]) +
                    "]] </div>\n")
                append_text(
                    "<div id=\"alignright\"> [[" +
                    secLabel(
                        sections[
                            (secCounter +
                             1) %
                            len(sections)][0]) +
                    "|" +
                    secLabel(
                        sections[
                            (secCounter +
                             1) %
                            len(sections)][0]) +
                    "]] >> </div>\n</div>\n\n")
                append_text("drmf_eof\n")
                sections[secCounter].append(eqCounter)
                eqCounter = 0

            elif "\\subsection" in line and parse:
                append_text("\n== " + getString(line) + " ==\n")
                head = True
            elif "\\paragraph" in line and parse:
                append_text("\n=== " + getString(line) + " ===\n")
                head = True
            elif "\\subsubsection" in line and parse:
                append_text("\n=== " + getString(line) + " ===\n")
                head = True

            elif "\\begin{equation}" in line and parse:
                if head:
                    append_text("\n")
                    head = False
                s_label = line.find("\\label{") + 7
                e_label = line.find("}", s_label)
                label = (line[s_label:e_label])
                eqCounter += 1
                for l_link in l_link_list:
                    if label == l_link[0:l_link.find("=") - 1]:
                        r_label = l_link[l_link.find("=>") + 3:l_link.find("\\n")]
                        r_label = r_label.replace("/", "")
                        r_label = r_label.replace("#", ":")
                        r_label = r_label.replace("!", ":")
                        break
                label = mod_label(r_label)
                labels.append("Formula:" + r_label)
                eqs.append("")
                append_text(
                    "<math id=\"" +
                    r_label.lstrip("Formula:") +
                    "\">\n")
                math = True
            elif "\\begin{equation}" in line and not parse:
                s_label = line.find("\\label{") + 7
                e_label = line.find("}", s_label)
                label = mod_label(line[s_label:e_label])
                labels.append("*" + label)  # special marker
                eqs.append("")
                math = True
            elif "\\end{equation}" in line:

                math = False
            elif "\\constraint" in line and parse:
                constraint = True
                math = False
                conLine = ""
            elif "\\substitution" in line and parse:
                substitution = True
                math = False
                subLine = ""
            elif "\\proof" in line and parse:
                math = False
            elif "\\drmfn" in line and parse:
                math = False
                if "\\drmfname" in line and parse:
                    append_text(
                        "<div align=\"right\">This formula has the name: " +
                        getString(line) +
                        "</div><br />\n")
            elif math and parse:
                flagM = True
                eqs[-1] += line

                if not (
                            (not (
                                        "\\end{equation}" in lines[
                                            i +
                                            1]) or "\\subsection" in lines[
                                    i +
                                    3]) or "\\section" in lines[
                                i +
                                3]) and not "\\part" in lines[
                            i +
                            3]:
                    u = i
                    flagM2 = False
                    while flagM:
                        u += 1
                        if "\\begin{equation}" in lines[u] in lines[u]:
                            flagM = False
                        if "\\section" in lines[u] or "\\subsection" in lines[
                            i] or "\\part" in lines[u] or "\\end{document}" in lines[u]:
                            flagM = False
                            flagM2 = True
                    if not flagM2:

                        append_text(line.rstrip("\n"))
                        append_text("\n</math><br />\n")
                    else:
                        append_text(line.rstrip("\n"))
                        append_text("\n</math>\n")
                elif "\\end{equation}" in lines[i + 1]:
                    append_text(line.rstrip("\n"))
                    append_text("\n</math>\n")
                elif "\\constraint" in lines[i + 1] or "\\substitution" in lines[i + 1] or "\\drmfn" in lines[i + 1]:
                    append_text(line.rstrip("\n"))
                    append_text("\n</math>\n")
                else:
                    append_text(line)
            elif math and not parse:
                eqs[-1] += line
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\drmfn" in lines[
                            i +
                            1]:
                    math = False
            if substitution and parse:
                subLine += line.replace("&", "&<br />")
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\drmfn" in lines[
                            i +
                            1] or "\\proof" in lines[
                            i +
                            1]:
                    substitution = False
                    append_text(
                        "<div align=\"right\">Substitution(s): " +
                        getEq(subLine) +
                        "</div><br />\n")

            if constraint and parse:
                conLine += line.replace("&", "&<br />")
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\drmfn" in lines[
                            i +
                            1] or "\\proof" in lines[
                            i +
                            1]:
                    constraint = False
                    append_text(
                        "<div align=\"right\">Constraint(s): " +
                        getEq(conLine) +
                        "</div><br />\n")

        eqCounter = n
        endNum = len(labels) - 1
        parse = False
        constraint = False
        substitution = False
        note = False
        hCon = True
        hSub = True
        hNote = True
        hProof = True
        proof = False
        comToWrite = ""
        secCount = -1
        newSec = False
        for i in range(0, len(lines)):
            line = lines[i]

            if "\\section" in line:
                secCount += 1
                newSec = True
                eqS = 0

            if "\\begin{equation}" in line:
                symLine = line.strip("\n")
                eqS += 1
                constraint = False
                substitution = False
                note = False
                comToWrite = ""
                hCon = True
                hSub = True
                hNote = True
                hProof = True
                proof = False
                parse = True
                symbols = []
                eqCounter += 1
                label = labels[eqCounter]
                append_revision(secLabel(label))
                append_text("{{DISPLAYTITLE:" + (labels[eqCounter]) + "}}\n")
                if eqCounter == len(labels) - 1:
                    break
                if eqCounter < endNum:  # FOR ANYTHING THAT IS NOT THE EXTRA EQUATIONS
                    append_text("<div id=\"drmf_head\">\n")
                    if newSec:
                        append_text(
                            "<div id=\"alignleft\"> "
                            "<< [[" +
                            secLabel(
                                sections[secCount][0]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                sections[secCount][0]) +
                            "]] </div>\n")
                    else:
                        append_text(
                            "<div id=\"alignleft\"> "
                            "<< [[" +
                            secLabel(
                                labels[
                                    eqCounter -
                                    1]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                labels[
                                    eqCounter -
                                    1]) +
                            "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        secLabel(
                            sections[
                                secCount +
                                1][0]).replace(
                            " ",
                            "_") +
                        "#" +
                        secLabel(
                            labels[eqCounter][
                            len("Formula:"):]) +
                        "|formula in " +
                        secLabel(
                            sections[
                                secCount +
                                1][0]) +
                        "]] </div>\n")
                    if True:
                        append_text(
                            "<div id=\"alignright\"> [[" +
                            secLabel(
                                labels[
                                    (eqCounter +
                                     1) %
                                    (endNum +
                                     1)]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                labels[
                                    (eqCounter +
                                     1) %
                                    (endNum +
                                     1)]) +
                            "]] >> </div>\n")
                    append_text("</div>\n\n")
                elif eqCounter == endNum:
                    append_text("<div id=\"drmf_head\">\n")
                    if newSec:
                        newSec = False
                        append_text(
                            "<div id=\"alignleft\"> << [[" +
                            secLabel(
                                sections[secCount][0]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                sections[secCount][0]) +
                            "]] </div>\n")
                    else:
                        append_text(
                            "<div id=\"alignleft\"> "
                            "<< [[" +
                            secLabel(
                                labels[
                                    eqCounter -
                                    1]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                labels[
                                    eqCounter -
                                    1]) +
                            "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        secLabel(
                            sections[
                                secCount +
                                1][0]).replace(
                            " ",
                            "_") +
                        "#" +
                        secLabel(
                            labels[eqCounter][
                            len("Formula:"):]) +
                        "|formula in " +
                        secLabel(
                            sections[
                                secCount +
                                1][0]) +
                        "]] </div>\n")
                    append_text(
                        "<div id=\"alignright\"> [[" +
                        secLabel(
                            labels[
                                (eqCounter +
                                 1) %
                                (endNum +
                                 1)].replace(
                                " ",
                                "_")) +
                        "|" +
                        secLabel(
                            labels[
                                (eqCounter +
                                 1) %
                                (endNum +
                                 1)]) +
                        "]] </div>\n")
                    append_text("</div>\n\n")

                append_text("<br /><div align=\"center\"><math> \n")
                math = True
            elif "\\end{equation}" in line:
                append_text(comToWrite)
                parse = False
                math = False
                if hProof:
                    append_text("\n== Proof ==\n\nWe ask users to provide proof(s), \
                    reference(s) to proof(s), or further clarification on the proof(s) in this space.\n")

                append_text("\n== Symbols List ==\n\n")
                newSym = []
                # if "09.07:04" in label:
                for x in symbols:
                    flagA = True
                    # if x not in newSym:
                    cN = 0
                    cC = 0
                    flag = True
                    ArgCx = 0
                    for z in x:
                        if z.isalpha() and flag or z == "&":
                            cN += 1
                        else:
                            flag = False
                            if z == "{" or z == "[":
                                cC += 1
                            if z == "}" or z == "]":
                                cC -= 1
                                if cC == 0:
                                    ArgCx += 1
                    noA = x[:cN]
                    for y in newSym:
                        cN = 0
                        cC = 0
                        ArgC = 0
                        flag = True
                        for z in y:
                            if z.isalpha() and flag or z == "&":
                                cN += 1
                            else:
                                flag = False
                                if z == "{" or z == "[":
                                    cC += 1
                                if z == "}" or z == "]":
                                    cC -= 1
                                    if cC == 0:
                                        ArgC += 1

                        if y[:cN] == noA:  # and ArgC==ArgCx:
                            flagA = False
                            break
                    if flagA:
                        newSym.append(x)
                newSym.reverse()
                ampFlag = False
                finSym = []
                for s in range(len(newSym) - 1, -1, -1):
                    symbolPar = "\\" + newSym[s]
                    ArgCx = 0
                    parCx = 0
                    parFlag = False
                    cC = 0
                    for z in symbolPar:
                        if z == "@":
                            parFlag = True
                        elif z.isalpha() or z == "&":
                            cN += 1
                        else:
                            if z == "{" or z == "[":
                                cC += 1
                            if z == "}" or z == "]":
                                cC -= 1
                                if cC == 0:
                                    if parFlag:
                                        parCx += 1
                                    else:
                                        ArgCx += 1

                    if symbolPar.find("{") != -1 or symbolPar.find("[") != -1:
                        if symbolPar.find("[") == -1:
                            symbol = symbolPar[0:symbolPar.find("{")]
                        elif symbolPar.find("{") == -1 or symbolPar.find("[") < symbolPar.find("{"):
                            symbol = symbolPar[0:symbolPar.find("[")]
                        else:
                            symbol = symbolPar[0:symbolPar.find("{")]
                    else:
                        symbol = symbolPar
                    gFlag = False
                    checkFlag = False
                    get = False
                    try:
                        gCSV = csv.reader(
                            open(
                                sys.argv[3],
                                'rb'),
                            delimiter=',',
                            quotechar='\"')
                    except (IOError, IndexError):
                        gCSV = csv.reader(
                            open(
                                '../../data/new.Glossary.csv',
                                'rb'),
                            delimiter=',',
                            quotechar='\"')
                    preG = ""
                    if symbol == "\\&":
                        ampFlag = True
                    for S in gCSV:
                        G = S
                        ArgCx = 0
                        parCx = 0
                        parFlag = False
                        cC = 0
                        ind = G[0].find("@")
                        if ind == -1:
                            ind = len(G[0]) - 1
                        for z in G[0]:
                            if z == "@":
                                parFlag = True
                            elif z.isalpha():
                                cN += 1
                            else:
                                if z == "{" or z == "[":
                                    cC += 1
                                if z == "}" or z == "]":
                                    cC -= 1
                                    if cC == 0:
                                        if parFlag:
                                            parCx += 1
                                        else:
                                            ArgCx += 1
                        if G[0].find(symbol) == 0 and (len(G[0]) == len(symbol) or not G[0][
                            len(symbol)].isalpha()):  # and (numPar!=0 or numArg!=0):
                            checkFlag = True
                            get = True
                            preG = S
                        elif checkFlag:
                            get = True
                            checkFlag = False
                        if get:
                            if get:
                                G = preG
                            if True:
                                if symbolPar.find("@") != -1:
                                    Q = symbolPar[:symbolPar.find("@")]
                                else:
                                    Q = symbolPar
                            listArgs = []
                            if len(Q) > len(symbol) and (Q[
                                                             len(symbol)] == "{" or Q[len(symbol)] == "["):
                                ap = ""
                                for o in range(len(symbol), len(Q)):
                                    if Q[o] == "{" or z == "[":
                                        pass
                                    elif Q[o] == "}" or z == "]":
                                        listArgs.append(ap)
                                        ap = ""
                                    else:
                                        ap += Q[o]
                            websiteF = ""
                            web1 = G[5]
                            for t in range(5, len(G)):
                                if G[t] != "":
                                    websiteF = websiteF + \
                                               " [" + G[t] + " " + G[t] + "]"
                            p1 = G[4].strip("$")
                            p1 = "<math>" + p1 + "</math>"
                            # if checkFlag:
                            new2 = ""
                            pause = False
                            mathF = True
                            p2 = G[1]
                            for k in range(0, len(p2)):
                                if p2[k] == "$":
                                    if mathF:
                                        new2 += "<math> "
                                    else:
                                        new2 += "</math>"
                                    mathF = not mathF
                                else:
                                    new2 += p2[k]
                            p2 = new2
                            finSym.append(
                                web1 + " " + p1 + "]</span> : " + p2 + " :" + websiteF)
                            break
                    if not gFlag:
                        del newSym[s]

                gFlag = True
                if ampFlag:
                    append_text("& : logical and")
                    gFlag = False
                for y in finSym:
                    if y == "& : logical and":
                        pass
                    elif gFlag:
                        gFlag = False
                        append_text("<span class=\"plainlinks\">[" + y)
                    else:
                        append_text("<br />\n<span class=\"plainlinks\">[" + y)

                append_text("\n<br />\n")

                # should there be a space between bibliography and ==?
                append_text("\n== Bibliography==\n\n")
                r = unmodLabel(labels[eqCounter])
                q = r.find("DLMF:") + 5
                p = r.find(":", q)
                section = r[q:p]
                equation = r[p + 1:]
                if equation.find(":") != -1:
                    equation = equation[0:equation.find(":")]
                if isnumber(section) == False:
                    return eqCounter
                append_text(
                    "<span class=\"plainlinks\">[HTTP://DLMF.NIST.GOV/" +
                    section +
                    "#" +
                    equation +
                    " Equation (" +
                    equation[
                    1:] +
                    "), Section " +
                    section +
                    "]</span> of [[Bibliography#DLMF|'''DLMF''']].\n\n")
                append_text(
                    "== URL links ==\n\nWe ask users to provide relevant URL links in this space.\n\n")
                if eqCounter < endNum:
                    append_text("<br /><div id=\"drmf_foot\">\n")
                    if newSec:
                        newSec = False
                        append_text(
                            "<div id=\"alignleft\"> << [[" +
                            secLabel(
                                sections[secCount][0]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                sections[secCount][0]) +
                            "]] </div>\n")
                    else:
                        append_text(
                            "<div id=\"alignleft\"> << [[" +
                            secLabel(
                                labels[
                                    eqCounter -
                                    1]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                labels[
                                    eqCounter -
                                    1]) +
                            "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        secLabel(
                            sections[
                                secCount +
                                1][0]).replace(
                            " ",
                            "_") +
                        "#" +
                        secLabel(
                            labels[eqCounter][
                            len("Formula:"):]) +
                        "|formula in " +
                        secLabel(
                            sections[
                                secCount +
                                1][0]) +
                        "]] </div>\n")
                    if True:
                        append_text(
                            "<div id=\"alignright\"> [[" +
                            secLabel(
                                labels[
                                    (eqCounter +
                                     1) %
                                    (endNum +
                                     1)]).replace(
                                " ",
                                "_") +
                            "|" +
                            secLabel(
                                labels[
                                    (eqCounter +
                                     1) %
                                    (endNum +
                                     1)]) +
                            "]] >> </div>\n")
                    append_text("</div>\n\ndrmf_eof\n")
                else:  # FOR EXTRA EQUATIONS
                    append_text("<br /><div id=\"drmf_foot\">\n")
                    append_text(
                        "<div id=\"alignleft\"> << [[" +
                        labels[
                            endNum -
                            1].replace(
                            " ",
                            "_") +
                        "|" +
                        labels[
                            endNum -
                            1] +
                        "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        labels[0].replace(
                            " ",
                            "_") +
                        "#" +
                        labels[endNum][
                        8:] +
                        "|formula in " +
                        labels[0] +
                        "]] </div>\n")
                    append_text(
                        "<div id=\"alignright\"> [[" +
                        labels[
                            (0) %
                            endNum].replace(
                            " ",
                            "_") +
                        "|" +
                        labels[
                            0 %
                            endNum] +
                        "]] </div>\n")
                    append_text("</div>\n\ndrmf_eof\n")

            elif "\\constraint" in line and parse:
                symLine = line.strip("\n")
                if hCon:
                    comToWrite += "\n== Constraint(s) ==\n\n"
                    hCon = False
                    constraint = True
                    math = False
                    conLine = ""
            elif "\\substitution" in line and parse:
                symLine = line.strip("\n")
                if hSub:
                    comToWrite += "\n== Substitution(s) ==\n\n"
                    hSub = False
                substitution = True
                math = False
                subLine = ""
            elif "\\drmfname" in line and parse:
                math = False
                comToWrite = "\n== Name ==\n\n<div align=\"left\">" + \
                             getString(line) + "</div><br />\n" + comToWrite

            elif "\\drmfnote" in line and parse:
                symbols = symbols + getSym(line)
                if hNote:
                    comToWrite += "\n== Note(s) ==\n\n"
                    hNote = False
                note = True
                math = False
                noteLine = ""

            elif "\\proof" in line and parse:
                symLine = line.strip("\n")
                if hProof:
                    hProof = False
                    comToWrite += "\n== Proof ==\n\nWe ask users to provide proof(s), reference(s) to proof(s), " \
                                  "or further clarification on the proof(s) in this space. \n<br /><br />\n<div align=\"left\">"
                proof = True
                proofLine = ""
                pause = False
                pauseP = False
                for ind in range(0, len(line)):
                    if line[ind:ind + 7] == "\\eqref{":
                        pause = True
                        eqR = line[ind:line.find("}", ind) + 1]
                        rLab = getString(eqR)
                        for l_link in l_link_list:
                            if rLab == l_link[0:l_link.find("=") - 1]:
                                r_label = l_link[l_link.find("=>") + 3:l_link.find("\\n")]
                                r_label = r_label.replace("/", "")
                                r_label = r_label.replace("#", ":")
                                r_label = r_label.replace("!", ":")
                                break

                        eInd = ref_labels.index("" + r_label)
                        z = line[line.find("}", ind + 7) + 1]
                        if z == "." or z == ",":
                            pauseP = True
                            proofLine += ("<br /> \n<math id=\"" +
                                          label +
                                          "\">\n" +
                                          ref_eqs[eInd] +
                                          "</math>" +
                                          z +
                                          "<br />\n")
                        else:
                            if z == "}":
                                proofLine += ("<br /> \n<math id=\"" +
                                              r_label +
                                              "\">\n" +
                                              ref_eqs[eInd] +
                                              "</math><br />")
                            else:
                                proofLine += ("<br /> \n<math id=\"" +
                                              r_label +
                                              "\">\n" +
                                              ref_eqs[eInd] +
                                              "</math><br />\n")
                    else:
                        if pause:
                            if line[ind] == "}":
                                pause = False
                        elif pauseP:
                            pauseP = False
                        elif line[ind] == "\n" and "\\end{equation}" in lines[i + 1]:
                            pass
                        else:
                            proofLine += (line[ind])
                if "\\end{equation}" in lines[i + 1]:
                    proof = False
                    append_text(
                        comToWrite +
                        getEqP(proofLine) +
                        "</div>\n<br />\n")
                    comToWrite = ""
                    symbols = symbols + getSym(symLine)
                    symLine = ""
            elif proof:
                symLine += line.strip("\n")
                pauseP = False
                for ind in range(0, len(line)):
                    if line[ind:ind + 7] == "\\eqref{":
                        pause = True
                        eqR = line[ind:line.find("}", ind) + 1]
                        rLab = getString(eqR)
                        for l_link in l_link_list:
                            if rLab == l_link[0:l_link.find("=") - 1]:
                                r_label = l_link[l_link.find("=>") + 3:l_link.find("\\n")]
                                r_label = r_label.replace("/", "")
                                r_label = r_label.replace("#", ":")
                                r_label = r_label.replace("!", ":")
                                break

                        eInd = ref_labels.index("" + r_label.lstrip("Formula:"))
                        z = line[line.find("}", ind + 7) + 1]
                        if z == "." or z == ",":
                            pauseP = True
                            proofLine += ("<br /> \n<math id=\"" +
                                          r_label +
                                          "\">\n" +
                                          ref_eqs[eInd] +
                                          "</math>" +
                                          z +
                                          "<br />\n")
                        else:
                            proofLine += ("<br /> \n<math id=\"" +
                                          r_label +
                                          "\">\n" +
                                          ref_eqs[eInd] +
                                          "</math><br />\n")

                    else:
                        if pause:
                            if line[ind] == "}":
                                pause = False
                        elif pauseP:
                            pauseP = False
                        elif line[ind] == "\n" and "\\end{equation}" in lines[i + 1]:
                            pass

                        else:
                            proofLine += (line[ind])
                if "\\end{equation}" in lines[i + 1]:
                    proof = False
                    append_text(
                        comToWrite +
                        getEqP(proofLine).rstrip("\n") +
                        "</div>\n<br />\n")
                    comToWrite = ""
                    symbols = symbols + getSym(symLine)
                    symLine = ""

            elif math:
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\proof" in lines[
                            i +
                            1] or "\\drmfnote" in lines[
                            i +
                            1] or "\\drmfname" in lines[
                            i +
                            1]:
                    append_text(line.rstrip("\n"))
                    symLine += line.strip("\n")
                    symbols = symbols + getSym(symLine)
                    symLine = ""
                    append_text("\n</math></div>\n")
                else:
                    symLine += line.strip("\n")
                    append_text(line)
            if note and parse:
                noteLine = noteLine + line
                symbols = symbols + getSym(line)
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\drmfn" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\proof" in lines[
                            i +
                            1]:
                    note = False
                    if "\\emph" in noteLine:
                        noteLine = noteLine[
                                   0:noteLine.find("\\emph{")] + "\'\'" + noteLine[
                                                                          noteLine.find("\\emph{") + len(
                                                                              "\\emph{"): noteLine.find(
                                                                              "}", noteLine.find("\\emph{") + len(
                                                                                  "\\emph{"))] + "\'\'" + noteLine[
                                                                                                          noteLine.find(
                                                                                                              "}",
                                                                                                              noteLine.find(
                                                                                                                  "\\emph{") + len(
                                                                                                                  "\\emph{")) + 1:]
                    comToWrite = comToWrite + "<div align=\"left\">" + \
                                 getEq(noteLine) + "</div><br />\n"

            if constraint and parse:
                conLine += line.replace("&", "&<br />")

                symLine += line.strip("\n")
                # symbols=symbols+getSym(line)
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\drmfn" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\proof" in lines[
                            i +
                            1]:
                    constraint = False
                    symbols = symbols + getSym(symLine)
                    symLine = ""
                    append_text(
                        comToWrite +
                        "<div align=\"left\">" +
                        getEq(conLine) +
                        "</div><br />\n")
                    comToWrite = ""
            if substitution and parse:
                subLine = subLine + line.replace("&", "&<br />")

                symLine += line.strip("\n")
                # symbols=symbols+getSym(line)
                if "\\end{equation}" in lines[
                            i +
                            1] or "\\drmfn" in lines[
                            i +
                            1] or "\\substitution" in lines[
                            i +
                            1] or "\\constraint" in lines[
                            i +
                            1] or "\\proof" in lines[
                            i +
                            1]:
                    substitution = False
                    symbols = symbols + getSym(symLine)
                    symLine = ""
                    append_text(
                        comToWrite +
                        "<div align=\"left\">" +
                        getEq(subLine) +
                        "</div><br />\n")
                    comToWrite = ""


if __name__ == "__main__":
    tex = "../../data/ZE.3.tex"
    mainFile = "../../data/OrthogonalPolynomials.mmd"
    lLinks = "../../data/BruceLabelLinks"
    dlmf(tex, mainFile, lLinks, 0)
