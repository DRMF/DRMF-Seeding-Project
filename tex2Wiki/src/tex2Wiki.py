__author__ = "Azeem Mohammed"
__status__ = "Development"

import csv
import sys
from shutil import copyfile
import xml.etree.ElementTree as ET
import datetime

wiki = ''
next_formula_number = 0
lLink = ''
ET.register_namespace('', 'http://www.mediawiki.org/xml/export-0.10/')
root = ET.Element('{http://www.mediawiki.org/xml/export-0.10/}mediawiki')


def isnumber(char):  # Function to check if char is a number (assuming 1 character)
    return char[0] in "0123456789"


def get_string(line):  # Gets all data within curly braces on a line
    # -------Initialization-------
    string_write = ""
    get_str = False
    p_w = ""
    # ----------------------------
    for c in line:
        if c == "{" or c == "}":  # if there is a curly brace in the line
            get_str = not get_str  # toggle the getStr flag
            if c == "}":  # no more info needed
                break
        elif get_str:  # if within curly braces
            if not (p_w == c and c == "-"):
                if c != "$":  # if not a $ sign
                    string_write += c  # this character is part of the data
                else:  # replace $ with ''
                    string_write += "\'\'"  # add double '
            p_w = c  # change last character for finding double dashes
    # return the data without newlines and without leading spaces
    return string_write.rstrip('\n').lstrip()


def get_g(line):  # gets equation for symbols list
    start = True
    final = ""
    for c in line:
        if c == "$" and start:
            final += "<math> "
            start = False
        elif c == "$":
            final += "</math>"
            start = True
        else:
            final += c
    return final


def get_eq(line):  # Gets all data within constraints,substitutions
    # -------Initialization-------
    per = 1
    string_write = ""
    f_eq = False
    count = 0
    # ----------------------------
    for c in line:  # read each character
        if count >= 0 and per != 0:
            per += 1
            if c != " " and c != "%":
                per = 0
        if c == "{" and per == 0:
            if count > 0:
                string_write += c
            count += 1
        elif c == "}" and per == 0:
            count -= 1
            if count > 0:
                string_write += c
        elif c == "$" and per == 0:  # either begin or end equation
            f_eq = not f_eq  # toggle fEq flag to know if begin or end equation
            if f_eq:  # if begin
                string_write += "<math>"
            else:  # if end
                string_write += "</math>"
        elif c == "\n" and per == 0:  # if newline
            string_write = string_write.strip()  # remove all leading and trailing whitespace

            # should above be
            # rstrip?<-------------------------------------------------------------------CHECK
            # THIS

            string_write += c  # add the newline character
            per += 1  # watch for % signs
        elif count > 0 and per == 0:  # not special character
            string_write += c  # write the character

    return string_write.rstrip().lstrip()


def get_eq_p(line):  # Gets all data within proofs
    per = 1
    string_write = ""
    f_eq = False
    count = 0
    length = 0
    for c in line:
        if f_eq and c != " " and c != "$" and \
            c != "{" and c != "}" and not c.isalpha():
            length += 1
        if count >= 0 and per != 0:
            per += 1
            if c != " " and c != "%":
                # if c!="%":
                per = 0
        if c == "{" and per == 0:
            if count > 0:
                string_write += c
            count += 1
        elif c == "}" and per == 0:
            count -= 1
            if count > 0:
                string_write += c
        elif c == "$" and per == 0:
            f_eq = not f_eq
            if f_eq:
                string_write += "<math> "
            else:
                if length < 10:
                    string_write += "</math>"
                else:
                    string_write += "</math>" + "<br />"
                length = 0
        elif c == "\n" and per == 0:
            string_write = string_write.strip()
            string_write += c
            per += 1
        elif count > 0 and per == 0:
            string_write += c

    return string_write.lstrip()


def get_sym(line):  # Gets all symbols on a line for symbols list
    sym_list = []
    if line == "":
        return sym_list
    symbol = ""
    sym_flag = False
    arg_flag = False
    cC = 0
    for i in range(0, len(line)):
        c = line[i]
        if sym_flag:
            if c == "{" or c == "[":
                cC += 1
                arg_flag = True
            if c != "}" and c != "]":
                if arg_flag or c.isalpha():
                    symbol += c
                else:
                    sym_flag = False
                    arg_flag = False
                    sym_list.append(symbol)
                    sym_list += (get_sym(symbol))
                    symbol = ""
            else:
                cC -= 1
                symbol += c
                if i + 1 == len(line):
                    p = ""
                else:
                    p = line[i + 1]
                if cC <= 0 and p != "{" and p != "[" and p != "@":
                    sym_flag = False
                    sym_list.append(symbol)
                    sym_list += (get_sym(symbol))
                    arg_flag = False
                    symbol = ""

        elif c == "\\":
            sym_flag = True
        elif c == "&" and not (i > line.find("\\begin{array}") and
                                       i < line.find("\\end{array}")):
            sym_list.append("&")

    sym_list.append(symbol)
    sym_list += get_sym(symbol)
    return sym_list


def unmod_label(label):
    label = label.replace(".0", ".")
    label = label.replace(":0", ":")
    return label


def sec_label(label):
    return label.replace("\'\'", "")


def mod_label(line):
    global lLink
    start_label = line.find("\\formula{")
    if start_label > 0:
        start_label += len("\\formula{")
    else:
        start_label = line.find("\\label{")
        if start_label > 0:
            start_label += len("\\label{")
        else:
            global next_formula_number
            next_formula_number += 1
            return 'auto-number-' + str(next_formula_number)
    end_label = line.find("}", start_label)
    label = line[start_label:end_label]
    rlabel = label
    for l in lLink:
        if l.find(label) != -1 and l[len(label) + 1] == "=":
            rlabel = l[l.find("=>") + 3:l.find("\\n")]
            rlabel = rlabel.replace("/", "")
            rlabel = rlabel.replace("#", ":")
            break
    label = rlabel
    label = label.replace('eq:', 'Formula:')
    is_numer = False
    newlabel = ""
    num = ""
    for i in range(0, len(label)):
        if is_numer and not isnumber(label[i]):
            if len(num) > 1:
                newlabel += num
                num = ""
            else:
                newlabel += "0" + str(num)
                num = ""
        if isnumber(label[i]):
            is_numer = True
            num += str(label[i])
        else:
            is_numer = False
            newlabel += label[i]
    if len(num) > 1:
        newlabel += num
    elif len(num) == 1:
        newlabel += "0" + num
    return newlabel


def append_text(text):
    global wiki
    wiki.text = wiki.text + text


def append_revision(param):
    global wiki
    page = ET.SubElement(root, 'page')
    title = ET.SubElement(page, 'title')
    title.text = param
    revision = ET.SubElement(page, 'revision')
    timestamp = ET.SubElement(revision, 'timestamp')
    timestamp.text = str(datetime.datetime.utcnow())
    contributor = ET.SubElement(revision, 'contributor')
    username = ET.SubElement(contributor, 'username')
    username.text = 'SeedBot'
    wiki = ET.SubElement(revision, 'text')
    wiki.text = ''


def writeout(ofname):
    tree = ET.ElementTree(root)
    tree.write(ofname, xml_declaration=True, encoding='utf-8', method='xml')


def main():
    if len(sys.argv) != 6:
        fname = "../../data/ZE.3.tex"
        ofname = "../../data/ZE.4.xml"
        lname = "../../data/BruceLabelLinks"
        glossary = "../../data/new.Glossary.csv"
        mmd = "../../data/OrthogonalPolynomials.mmd"

    else:
        fname = sys.argv[1]
        ofname = sys.argv[2]
        lname = sys.argv[3]
        glossary = sys.argv[4]
        mmd = sys.argv[5]
    setup_label_links(lname)
    readin(fname, glossary, mmd)
    writeout(ofname)


def setup_label_links(ofname):
    global lLink
    lLink = open(ofname, "r").readlines()


def readin(ofname, glossary, mmd):
    # try:
    for iterations in range(0, 1):
        tex = open(ofname, 'r')
        main_file = open(mmd, "r")
        main_text = main_file.read()
        main_prepend = ""
        main_write = open("OrthogonalPolynomials.mmd.new", "w")
        glossary = open('new.Glossary.csv', 'rb')
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
        ref_labels = []
        chapter = ''
        for i in range(0, len(ref_lines)):
            line = ref_lines[i]
            if "\\begin{equation}" in line:
                label = mod_label(line)
                ref_labels.append(label)
                ref_eqs.append("")
                math = True
            elif math:
                ref_eqs[-1] += line
                if "\\end{equation}" in ref_lines[i + 1] or \
                        "\\constraint" in ref_lines[i + 1] or \
                        "\\substitution" in ref_lines[i + 1] or \
                        "\\drmfn" in ref_lines[i + 1]:
                    math = False

        for i in range(0, len(lines)):
            line = lines[i]
            if "\\begin{document}" in line:
                parse = True
            elif "\\end{document}" in line and parse:
                main_prepend += "</div>\n"
                main_text = main_prepend + main_text
                main_text = main_text.replace(
                    "\'\'\'Orthogonal Polynomials\'\'\'\n", "")
                main_text = main_text.replace("{{#set:Section=0}}\n", "")
                main_text = main_text[0:main_text.rfind("== Sections ")]
                append_revision('Orthogonal Polynomials')
                main_text = "{{#set:Section=0}}\n" + main_text
                main_write.write(main_text)
                main_write.close()
                main_file.close()
                copyfile(mmd, 'OrthogonalPolynomials.mmd.new')
                parse = False
            elif "\\title" in line and parse:
                string_write = "\'\'\'"
                string_write += get_string(line) + "\'\'\'\n"
                labels.append("Orthogonal Polynomials")
                sections.append(["Orthogonal Polynomials", 0])
                chapter = get_string(line)
                main_prepend += ("\n== Sections in " +
                                chapter +
                                " ==\n\n<div style=\"-moz-column-count:2; " +
                                "column-count:2;-webkit-column-count:2\">\n")
            elif "\\part" in line:
                if get_string(line) == "BOF":
                    parse = False
                elif get_string(line) == "EOF":
                    parse = True
                elif parse:
                    main_prepend += ("\n<br />\n= " + get_string(line) + " =\n")
                    head = True
            elif "\\section" in line:
                main_prepend += "* [[" + sec_label(get_string(line)) + "|" + \
                                get_string(line) + "]]\n"
                sections.append([get_string(line)])

        sec_counter = 0
        eq_counter = 0
        sub_line = ''
        con_line = ''
        for i in range(0, len(lines)):
            line = lines[i]
            if "\\section" in line:
                parse = True
                sec_counter += 1
                append_revision(sec_label(get_string(line)))
                append_text(
                    "{{DISPLAYTITLE:" + (sections[sec_counter][0]) + "}}\n")
                append_text("{{#set:Chapter=" + chapter + "}}\n")
                append_text("{{#set:Section=" + str(sec_counter) + "}}\n")
                append_text("{{headSection}}\n")
                head = True
                append_text("== " + get_string(line) + " ==\n")
            elif ("\\section" in lines[(i + 1) % len(lines)] or
                          "\\end{document}" in lines[
                    (i + 1) % len(lines)]) and parse:
                append_text("{{footSection}}\n")
                sections[sec_counter].append(eq_counter)
                eq_counter = 0

            elif "\\subsection" in line and parse:
                append_text("\n== " + get_string(line) + " ==\n")
                head = True
            elif "\\paragraph" in line and parse:
                append_text("\n=== " + get_string(line) + " ===\n")
                head = True
            elif "\\subsubsection" in line and parse:
                append_text("\n=== " + get_string(line) + " ===\n")
                head = True

            elif "\\begin{equation}" in line and parse:
                if head:
                    append_text("\n")
                    head = False
                label = mod_label(line)
                eq_counter += 1
                labels.append(label)
                eqs.append("")
                append_text("<math id=\"" + label.lstrip("Formula:") + "\">")
                math = True
            elif "\\begin{equation}" in line and not parse:
                label = mod_label(line)
                labels.append("*" + label)  # special marker
                eqs.append("")
                math = True
            elif "\\end{equation}" in line:

                math = False
            elif "\\constraint" in line and parse:
                constraint = True
                math = False
                con_line = ""
            elif "\\substitution" in line and parse:
                substitution = True
                math = False
                sub_line = ""
            elif "\\proof" in line and parse:
                math = False
            elif "\\drmfn" in line and parse:
                math = False
                if "\\drmfname" in line and parse:
                    append_text(
                        "<div align=\"right\">This formula has the name: " +
                        get_string(line) +
                        "</div><br />\n")
            elif math and parse:
                flag_m = True
                eqs[-1] += line

                if "\\end{equation}" in lines[i + 1] and \
                        "\\subsection" not in lines[i + 3] and \
                        "\\section" not in lines[i + 3] and \
                        "\\part" not in lines[i + 3]:
                    u = i
                    flag_m2 = False
                    while flag_m:
                        u += 1
                        if "\\begin{equation}" in lines[u] in lines[u]:
                            flag_m = False
                        if "\\section" in lines[u] or \
                                "\\subsection" in lines[i] or \
                                "\\part" in lines[u] or \
                                "\\end{document}" in lines[u]:
                            flag_m = False
                            flag_m2 = True
                    if not flag_m2:

                        append_text(line.rstrip("\n"))
                        append_text("\n</math><br />\n")
                    else:
                        append_text(line.rstrip("\n"))
                        append_text("\n</math>\n")
                elif "\\end{equation}" in lines[i + 1]:
                    append_text(line.rstrip("\n"))
                    append_text("\n</math>\n")
                elif "\\constraint" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1]:
                    append_text(line.rstrip("\n"))
                    append_text("\n</math>\n")
                else:
                    append_text(line)
            elif math and not parse:
                eqs[-1] += line
                if "\\end{equation}" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1]:
                    math = False
            if substitution and parse:
                sub_line += line.replace("&", "&<br />")
                if "\\end{equation}" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1] or \
                        "\\proof" in lines[i + 1]:
                    line_r = ""
                    for i in range(0, len(sub_line)):
                        if sub_line[i] == "&" and \
                                not (i > sub_line.find("\\begin{array}") and
                                             i < sub_line.find("\\end{array}")):
                            line_r += "&<br />"
                        else:
                            line_r += sub_line[i]
                    substitution = False
                    append_text(
                        "<div align=\"right\">Substitution(s): " +
                        get_eq(sub_line) +
                        "</div><br />\n")

            if constraint and parse:
                con_line += line.replace("&", "&<br />")
                if "\\end{equation}" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1] or \
                        "\\proof" in lines[i + 1]:
                    constraint = False
                    append_text(
                        "<div align=\"right\">Constraint(s): " +
                        get_eq(con_line) +
                        "</div><br />\n")

        eq_counter = 0
        end_num = len(labels) - 1
        parse = False
        constraint = False
        substitution = False
        note = False
        h_con = True
        h_sub = True
        h_note = True
        h_proof = True
        proof = False
        com_to_write = ""
        sec_count = -1
        new_sec = False
        sym_line = ''
        eqS = ''
        note_line = ''
        proof_line = ''
        pause = False
        for i in range(0, len(lines)):
            line = lines[i]

            if "\\section" in line:
                sec_count += 1
                new_sec = True
                eqS = 0

            if "\\begin{equation}" in line:
                sym_line = line.strip("\n")
                eqS += 1
                constraint = False
                substitution = False
                note = False
                com_to_write = ""
                h_con = True
                h_sub = True
                h_note = True
                h_proof = True
                proof = False
                parse = True
                symbols = []
                eq_counter += 1
                label = labels[eq_counter]
                append_revision(sec_label(label))
                append_text("{{DISPLAYTITLE:" + (labels[eq_counter]) + "}}\n")
                if eq_counter < end_num:
                    append_text("<div id=\"drmf_head\">\n")
                    if new_sec:
                        append_text("<div id=\"alignleft\"> << [[" +
                                    sec_label(sections[sec_count][0])
                                    .replace(" ", "_") + "|" +
                                    sec_label(sections[sec_count][0]) +
                                    "]] </div>\n")
                    else:
                        append_text("<div id=\"alignleft\"> << [[" +
                                    sec_label(labels[eq_counter - 1])
                                    .replace(" ", "_") + "|" +
                                    sec_label(labels[eq_counter - 1]) +
                                    "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        sec_label(sections[sec_count + 1][0])
                        .replace(" ", "_") + "#" +
                        sec_label(labels[eq_counter][len("Formula:"):]) +
                        "|formula in " +
                        sec_label(sections[sec_count + 1][0]) + "]] </div>\n")
                    if eqS == sections[sec_count][1]:
                        append_text("<div id=\"alignright\"> [[" +
                                    sec_label(
                                        sections[(sec_count + 1) %
                                                 len(sections)][0])
                                    .replace(" ", "_") + "|" +
                                    sec_label(sections[(sec_count + 1) %
                                                       len(sections)][0]) +
                                    "]] >> </div>\n")
                    else:
                        append_text("<div id=\"alignright\"> [[" +
                                    sec_label(
                                        labels[(eq_counter + 1) %
                                               (end_num + 1)])
                                    .replace(" ", "_") + "|" +
                                    sec_label(
                                        labels[(eq_counter + 1) %
                                               (end_num + 1)]) +
                                    "]] >> </div>\n")
                    append_text("</div>\n\n")
                elif eq_counter == end_num:
                    append_text("<div id=\"drmf_head\">\n")
                    if new_sec:
                        new_sec = False
                        append_text(
                            "<div id=\"alignleft\"> << [[" +
                            sec_label(
                                sections[sec_count][0]).replace(" ", "_") +
                            "|" + sec_label(sections[sec_count][0]) +
                            "]] </div>\n")
                    else:
                        append_text(
                            "<div id=\"alignleft\"> << [[" +
                            sec_label(
                                labels[eq_counter - 1])
                            .replace(" ", "_") + "|" +
                            sec_label(labels[eq_counter - 1]) + "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        sec_label(
                            sections[sec_count + 1][0]).replace(" ", "_") +
                        "#" + sec_label(labels[eq_counter][len("Formula:"):]) +
                        "|formula in " + sec_label(sections[sec_count + 1][0]) +
                        "]] </div>\n")
                    append_text(
                        "<div id=\"alignright\"> [[" +
                        sec_label(
                            labels[(eq_counter + 1) % (end_num + 1)]
                            .replace(" ", "_")) + "|" +
                        sec_label(
                            labels[(eq_counter + 1) % (end_num + 1)]) +
                        "]] </div>\n")
                    append_text("</div>\n\n")

                append_text("<br /><div align=\"center\"><math> \n")
                math = True
            elif "\\end{equation}" in line:
                append_text(com_to_write)
                parse = False
                math = False
                if h_proof:
                    append_text("\n== Proof ==\n\nWe ask users to provide "
                                "proof(s), reference(s) to proof(s), or"
                                " further clarification on the proof(s) "
                                "in this space.\n")
                append_text("\n== Symbols List ==\n\n")
                new_sym = []
                for x in symbols:
                    flagA = True
                    c_n = 0
                    c_c = 0
                    flag = True
                    arg_cx = 0
                    for z in x:
                        if z.isalpha() and flag or z == "&":
                            c_n += 1
                        else:
                            flag = False
                            if z == "{" or z == "[":
                                c_c += 1
                            if z == "}" or z == "]":
                                c_c -= 1
                                if c_c == 0:
                                    arg_cx += 1
                    no_a = x[:c_n]
                    for y in new_sym:
                        c_n = 0
                        c_c = 0
                        arg_c = 0
                        flag = True
                        for z in y:
                            if z.isalpha() and flag or z == "&":
                                c_n += 1
                            else:
                                flag = False
                                if z == "{" or z == "[":
                                    c_c += 1
                                if z == "}" or z == "]":
                                    c_c -= 1
                                    if c_c == 0:
                                        arg_c += 1

                        if y[:c_n] == no_a:
                            flagA = False
                            break
                    if flagA:
                        new_sym.append(x)
                new_sym.reverse()
                amp_flag = False
                fin_sym = []
                for s in range(len(new_sym) - 1, -1, -1):
                    symbol_par = "\\" + new_sym[s]
                    arg_cx = 0
                    par_cx = 0
                    par_flag = False
                    c_c = 0
                    c_n = 0
                    for z in symbol_par:
                        if z == "@":
                            par_flag = True
                        elif z.isalpha() or z == "&":
                            c_n += 1
                        else:
                            if z == "{" or z == "[":
                                c_c += 1
                            if z == "}" or z == "]":
                                c_c -= 1
                                if c_c == 0:
                                    if par_flag:
                                        par_cx += 1
                                    else:
                                        arg_cx += 1

                    if symbol_par.find("{") != -1 or symbol_par.find("[") != -1:
                        if symbol_par.find("[") == -1:
                            symbol = symbol_par[0:symbol_par.find("{")]
                        elif symbol_par.find("{") == -1 or \
                            symbol_par.find("[") < symbol_par.find("{"):
                            symbol = symbol_par[0:symbol_par.find("[")]
                        else:
                            symbol = symbol_par[0:symbol_par.find("{")]
                    else:
                        symbol = symbol_par
                    g_flag = False
                    check_flag = False
                    get = False
                    g_c_s_v = csv.reader(open(glossary, 'rb'),
                                         delimiter=',', quotechar='\"')
                    pre_g = ""
                    if symbol == "\\&":
                        amp_flag = True
                    for S in g_c_s_v:
                        g = S
                        arg_cx = 0
                        par_cx = 0
                        par_flag = False
                        c_c = 0
                        ind = g[0].find("@")
                        if ind == -1:
                            ind = len(g[0]) - 1
                        for z in g[0]:
                            if z == "@":
                                par_flag = True
                            elif z.isalpha():
                                c_n += 1
                            else:
                                if z == "{" or z == "[":
                                    c_c += 1
                                if z == "}" or z == "]":
                                    c_c -= 1
                                    if c_c == 0:
                                        if par_flag:
                                            par_cx += 1
                                        else:
                                            arg_cx += 1
                        if g[0].find(symbol) == 0 and \
                            len(g[0]) == len(symbol) or \
                                not g[0][len(symbol)].isalpha():
                            check_flag = True
                            get = True
                            pre_g = S
                        elif check_flag:
                            get = True
                            check_flag = False
                        if get:
                            if get:
                                g = pre_g
                            if True:
                                if symbol_par.find("@") != -1:
                                    q = symbol_par[:symbol_par.find("@")]
                                else:
                                    q = symbol_par
                            list_args = []
                            if len(q) > len(symbol) and \
                                    (q[len(symbol)] == "{" or
                                             q[len(symbol)] == "["):
                                ap = ""
                                for o in range(len(symbol), len(q)):
                                    if q[o] == "}" or z == "]":
                                        list_args.append(ap)
                                        ap = ""
                                    else:
                                        ap += q[o]
                            website_f = ""
                            web1 = g[5]
                            for t in range(5, len(g)):
                                if g[t] != "":
                                    website_f += " [" + g[t] + " " + g[t] + "]"
                            p1 = g[4].strip("$")
                            p1 = "<math>" + p1 + "</math>"
                            new2 = ""
                            pause = False
                            math_f = True
                            p2 = g[1]
                            for k in range(0, len(p2)):
                                if p2[k] == "$":
                                    if math_f:
                                        new2 += "<math> "
                                    else:
                                        new2 += "</math>"
                                    math_f = not math_f
                                else:
                                    new2 += p2[k]
                            p2 = new2
                            fin_sym.append(web1 + " " + p1 + "]</span> : " +
                                          p2 + " :" + website_f)
                            break
                    if not g_flag:
                        del new_sym[s]

                g_flag = True
                if amp_flag:
                    append_text("& : logical and")
                    g_flag = False
                for y in fin_sym:
                    if y == "& : logical and":
                        pass
                    elif g_flag:
                        g_flag = False
                        append_text("<span class=\"plainlinks\">[" + y)
                    else:
                        append_text("<br />\n<span class=\"plainlinks\">[" + y)

                append_text("\n<br />\n")

                # should there be a space between bibliography and ==?
                append_text("\n== Bibliography==\n\n")
                r = unmod_label(labels[eq_counter])
                q = r.find("KLS:") + 4
                p = r.find(":", q)
                section = r[q:p]
                equation = r[p + 1:]
                if equation.find(":") != -1:
                    equation = equation[0:equation.find(":")]
                append_text(
                    "<span class=\"plainlinks\">["
                    "http://homepage.tudelft.nl/11r49/askey/contents.html "
                    "Equation in Section " +
                    section +
                    "]</span> of [[Bibliography#KLS|'''KLS''']].\n\n")
                append_text(
                    "== URL links ==\n\nWe ask users to provide relevant URL "
                    "links in this space.\n\n")
                if eq_counter < end_num:
                    append_text("<br /><div id=\"drmf_foot\">\n")
                    if new_sec:
                        new_sec = False
                        append_text("<div id=\"alignleft\"> << [[" +
                                    sec_label(sections[sec_count][0])
                                    .replace(" ", "_") + "|" +
                                    sec_label(sections[sec_count][0]) +
                                    "]] </div>\n")
                    else:
                        append_text("<div id=\"alignleft\"> << [[" +
                                    sec_label(labels[eq_counter - 1])
                                    .replace(" ", "_") + "|" +
                                    sec_label(labels[eq_counter - 1]) +
                                    "]] </div>\n")
                    append_text("<div id=\"aligncenter\"> [[" +
                                sec_label(sections[sec_count + 1][0])
                                .replace(" ", "_") + "#" +
                                sec_label(labels[eq_counter][len("Formula:"):]) +
                                "|formula in " +
                                sec_label(sections[sec_count + 1][0]) +
                                "]] </div>\n")
                    if eqS == sections[sec_count][1]:
                        append_text(
                            "<div id=\"alignright\"> [[" +
                            sections[(sec_count + 1) % len(sections)][0]
                            .replace(" ", "_") + "|" +
                            sections[(sec_count + 1) % len(sections)][0] +
                            "]] >> </div>\n")
                    else:
                        append_text(
                            "<div id=\"alignright\"> [[" +
                            sec_label(labels[(eq_counter + 1) %
                                             (end_num + 1)])
                            .replace(" ", "_") + "|" +
                            sec_label(labels[(eq_counter + 1) %
                                             (end_num + 1)]) +
                            "]] >> </div>\n")
                    append_text("</div>\n")
                else:  # FOR EXTRA EQUATIONS
                    append_text("<br /><div id=\"drmf_foot\">\n")
                    append_text(
                        "<div id=\"alignleft\"> << [[" +
                        labels[end_num - 1].replace(" ", "_") + "|" +
                        labels[end_num - 1] + "]] </div>\n")
                    append_text(
                        "<div id=\"aligncenter\"> [[" +
                        labels[0].replace(" ", "_") + "#" +
                        labels[end_num][8:] + "|formula in " + labels[0] +
                        "]] </div>\n")
                    append_text(
                        "<div id=\"alignright\"> [[" +
                        labels[0 % end_num].replace(" ", "_") + "|" +
                        labels[0 % end_num] + "]] </div>\n")
                    append_text("</div>\n")
            elif "\\constraint" in line and parse:
                sym_line = line.strip("\n")
                if h_con:
                    com_to_write += "\n== Constraint(s) ==\n\n"
                    h_con = False
                    constraint = True
                    math = False
                    con_line = ""
            elif "\\substitution" in line and parse:
                sym_line = line.strip("\n")
                if h_sub:
                    com_to_write += "\n== Substitution(s) ==\n\n"
                    h_sub = False
                substitution = True
                math = False
                sub_line = ""
            elif "\\drmfname" in line and parse:
                math = False
                com_to_write = "\n== Name ==\n\n<div align=\"left\">" + \
                               get_string(line) + "</div><br />\n" + com_to_write
            elif "\\drmfnote" in line and parse:
                symbols = symbols + get_sym(line)
                if h_note:
                    com_to_write += "\n== Note(s) ==\n\n"
                    h_note = False
                note = True
                math = False
                note_line = ""
            elif "\\proof" in line and parse:
                sym_line = line.strip("\n")
                if h_proof:
                    h_proof = False
                    com_to_write +=\
                        "\n== Proof ==\n\nWe ask users to provide proof(s), " \
                        "reference(s) to proof(s), or further clarification " \
                        "on the proof(s) in this space. \n<br /><br />\n" \
                        "<div align=\"left\">"
                proof = True
                proof_line = ""
                pause = False
                pause_p = False
                for ind in range(0, len(line)):
                    if line[ind:ind + 7] == "\\eqref{":
                        # TODO: figure out how eqR is defined
                        pause = True
                        eInd = ref_labels.index(
                            "" + label)  # this should be rLab
                        z = line[line.find("}", ind + 7) + 1]
                        if z == "." or z == ",":
                            pause_p = True
                            pause_p = True
                            proof_line += ("<br /> \n<math id=\"" + label +
                                           "\">" + ref_eqs[eInd] + "</math>" +
                                           z + "<br />\n")
                        else:
                            if z == "}":
                                proof_line += ("<br /> \n<math id=\"" + label +
                                               "\">" + ref_eqs[eInd] +
                                               "</math><br />")
                            else:
                                proof_line += ("<br /> \n<math id=\"" + label +
                                               "\"> \n" + ref_eqs[eInd] +
                                               "</math><br />\n")
                    else:
                        if pause:
                            if line[ind] == "}":
                                pause = False
                        elif pause_p:
                            pause_p = False
                        elif line[ind] == "\n" and \
                             "\\end{equation}" in lines[i + 1]:
                            pass
                        else:
                            proof_line += (line[ind])
                if "\\end{equation}" in lines[i + 1]:
                    proof = False
                    append_text(com_to_write + get_eq_p(proof_line) +
                                "</div>\n<br />\n")
                    com_to_write = ""
                    symbols = symbols + get_sym(sym_line)
                    sym_line = ""

            elif proof:
                sym_line += line.strip("\n")
                pause_p = False
                for ind in range(0, len(line)):
                    if line[ind:ind + 7] == "\\eqref{":
                        pause = True
                        # TODO: Figure out how this is used
                        eInd = ref_labels.index("" + label)
                        z = line[line.find("}", ind + 7) + 1]
                        if z == "." or z == ",":
                            pause_p = True
                            proof_line += ("<br /> \n<math id=\"" + label +
                                          "\">" + ref_eqs[eInd] + "</math>" +
                                          z + "<br />\n")
                        else:
                            proof_line += ("<br /> \n<math id=\"" + label +
                                          "\">" + ref_eqs[eInd] +
                                          "</math><br />\n")

                    else:
                        if pause:
                            if line[ind] == "}":
                                pause = False
                        elif pause_p:
                            pause_p = False
                        elif line[ind] == "\n" and \
                                        "\\end{equation}" in lines[i + 1]:
                            pass

                        else:
                            proof_line += (line[ind])
                if "\\end{equation}" in lines[i + 1]:
                    proof = False
                    append_text(com_to_write + get_eq_p(proof_line).rstrip("\n") +
                                "</div>\n<br />\n")
                    com_to_write = ""
                    symbols = symbols + get_sym(sym_line)
                    sym_line = ""

            elif math:
                if "\\end{equation}" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\proof" in lines[i + 1] or \
                        "\\drmfnote" in lines[i + 1] or \
                        "\\drmfname" in lines[i + 1]:
                    append_text(line.rstrip("\n"))
                    sym_line += line.strip("\n")
                    symbols = symbols + get_sym(sym_line)
                    sym_line = ""
                    append_text("\n</math></div>\n")
                else:
                    sym_line += line.strip("\n")
                    append_text(line)
            if note and parse:
                note_line += line
                symbols = symbols + get_sym(line)
                if "\\end{equation}" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\proof" in lines[i + 1]:
                    note = False
                    if "\\emph" in note_line:
                        note_line = note_line[
                            0:note_line.find("\\emph{")] + "\'\'" + \
                                   note_line[
                                   note_line.find("\\emph{") + len(
                                       "\\emph{"):note_line.find(
                                       "}", note_line.find("\\emph{") + len(
                                           "\\emph{"))] + "\'\'" + \
                                   note_line[
                                   note_line.find("}", note_line.find(
                                       "\\emph{") + len("\\emph{")) + 1:]
                    com_to_write = com_to_write + "<div align=\"left\">" + \
                                   get_eq(note_line) + "</div><br />\n"

            if constraint and parse:
                con_line += line.replace("&", "&<br />")

                sym_line += line.strip("\n")
                # symbols=symbols+get_sym(line)
                if "\\end{equation}" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\proof" in lines[i + 1]:
                    constraint = False
                    symbols = symbols + get_sym(sym_line)
                    sym_line = ""
                    append_text(com_to_write + "<div align=\"left\">" +
                                get_eq(con_line) + "</div><br />\n")
                    com_to_write = ""
            if substitution and parse:
                # TODO: Figure out if .replace is needed
                sub_line += line.replace("&", "&<br />")

                sym_line += line.strip("\n")
                if "\\end{equation}" in lines[i + 1] or \
                        "\\drmfn" in lines[i + 1] or \
                        "\\substitution" in lines[i + 1] or \
                        "\\constraint" in lines[i + 1] or \
                        "\\proof" in lines[i + 1]:
                    substitution = False
                    symbols = symbols + get_sym(sym_line)
                    sym_line = ""
                    line_r = ""
                    for i in range(0, len(sub_line)):
                        if sub_line[i] == "&" and \
                            not (i > sub_line.find("\\begin{array}") and
                                 i < sub_line.find("\\end{array}")):
                            line_r += "&<br />"
                        else:
                            line_r += sub_line[i]
                    append_text(com_to_write + "<div align=\"left\">" +
                                get_eq(sub_line) + "</div><br />\n")
                    com_to_write = ""


if __name__ == "__main__":
    main()
