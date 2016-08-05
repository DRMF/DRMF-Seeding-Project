__author__ = "Azeem Mohammed"
__status__ = "Development"
__credits__ = ["Joon Bang", "Azeem Mohammed"]

import csv

GLOSSARY_LOCATION = "new.Glossary.csv"


def get_symbols(line):
    # (str) -> list
    """Gets all symbols on a line."""
    line = line.replace("\n", " ")
    sym_list = []
    if line == "":
        return sym_list

    symbol = ""
    sym_flag = False
    arg_flag = False
    count = 0

    for i in range(len(line)):
        ch = line[i]
        if sym_flag:
            if ch == "{" or ch == "[":
                count += 1
                arg_flag = True

            if ch != "}" and ch != "]":
                if arg_flag or ch.isalpha():
                    symbol += ch
                else:
                    sym_flag = False
                    arg_flag = False
                    sym_list.append(symbol)
                    sym_list += (get_symbols(symbol))
                    symbol = ""
            else:
                count -= 1
                symbol += ch
                if i + 1 == len(line):
                    p = ""
                else:
                    p = line[i + 1]
                if count == 0 and p != "{" and p != "[" and p != "@":
                    sym_flag = False
                    sym_list.append(symbol)
                    sym_list += (get_symbols(symbol))
                    arg_flag = False
                    symbol = ""

        elif ch == "\\":
            sym_flag = True

    sym_list.append(symbol)
    sym_list += get_symbols(symbol)
    return sym_list


def main(data):
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

        symbols = get_symbols((' '.join(page.split("\n")) + " ").replace("\n", " "))

        new_symbols = []

        for symbol in symbols:
            flag_a = True
            flag_b = True
            c_n = 0
            c_c = 0
            arg_count = 0

            for ch in symbol:
                if ch.isalpha() and flag_a:
                    c_n += 1
                else:
                    flag_a = False
                    if ch == "{" or ch == "[":
                        c_c += 1
                    if ch == "}" or ch == "]":
                        c_c -= 1
                        if c_c == 0:
                            arg_count += 1
            noA = symbol[:c_n]

            for y in new_symbols:
                c_n = 0
                c_c = 0
                arg_count = 0
                flag_a = True
                for ch in y:
                    if ch.isalpha() and flag_a:
                        c_n += 1
                    else:
                        flag_a = False
                        if ch == "{" or ch == "[":
                            c_c += 1
                        if ch == "}" or ch == "]":
                            c_c -= 1
                            if c_c == 0:
                                arg_count += 1

                if y[:c_n].strip() == noA.strip():
                    flag_b = False
                    break

            if flag_b:
                new_symbols.append(symbol)

        new_symbols.reverse()
        final_symbols = []

        for i in xrange(len(new_symbols) - 1, -1, -1):
            symbolPar = "\\" + new_symbols[i]
            arg_count = 0
            par_count = 0
            parFlag = False
            c_c = 0
            for ch in symbolPar:
                if ch == "@":
                    parFlag = True
                elif ch.isalpha():
                    c_n += 1
                elif ch == "{" or ch == "[":
                    c_c += 1
                elif ch == "}" or ch == "]":
                    c_c -= 1
                    if c_c == 0:
                        if parFlag:
                            par_count += 1
                        else:
                            arg_count += 1

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

            glossary = csv.reader(open(GLOSSARY_LOCATION, "rb"), delimiter=',', quotechar='\"')

            preG = ""
            symbol = symbol.strip("}").strip("]")
            for S in glossary:
                G = S
                arg_count = 0
                par_count = 0
                parFlag = False
                c_c = 0
                ind = G[0].find("@")
                if ind == -1:
                    ind = len(G[0]) - 1
                for ch in G[0]:
                    if ch == "@":
                        parFlag = True
                    elif ch.isalpha():
                        c_n += 1
                    else:
                        if ch == "{" or ch == "[":
                            c_c += 1
                        if ch == "}" or ch == "]":
                            c_c -= 1
                            if c_c == 0:
                                if parFlag:
                                    par_count += 1
                                else:
                                    arg_count += 1
                if G[0].find(symbol) == 0 and (len(G[0]) == len(symbol) or not G[0][
                        len(symbol)].isalpha()):
                    checkFlag = True
                    get = True
                    preG = S
                elif checkFlag:
                    checkFlag = False
                    get = True

                if get:
                    G = preG

                    if symbolPar.find("@") != -1:
                        Q = symbolPar[:symbolPar.find("@")]
                    else:
                        Q = symbolPar

                    arg_list = []
                    if len(Q) > len(symbol) and (Q[len(symbol)] == "{" or Q[len(symbol)] == "["):
                        ap = ""
                        for o in xrange(len(symbol), len(Q)):
                            if Q[o] == "}" or ch == "]":
                                arg_list.append(ap)
                                ap = ""
                            elif Q[o] != "{" and ch != "[":
                                ap += Q[o]

                    websiteF = ""
                    web1 = G[5]
                    for t in xrange(5, len(G)):
                        if G[t] != "":
                            websiteF = websiteF + " [" + G[t] + " " + G[t] + "]"

                    p1 = G[4].strip("$")
                    p1 = "<math>{\\displaystyle " + p1 + "}</math>"
                    new2 = ""
                    mathF = True
                    p2 = G[1]
                    for k in p2:
                        if k == "$":
                            if mathF:
                                new2 += "<math>{\\displaystyle "
                            else:
                                new2 += "}</math>"
                            mathF = not mathF
                        else:
                            new2 += k
                    p2 = new2
                    final_symbols.append(web1 + " " + p1 + "]</span> : " + p2 + " :" + websiteF)
                    break

            if not gFlag:
                new_symbols.pop(i)

        gFlag = True
        for y in final_symbols:
            if gFlag:
                gFlag = False
                to_write += ("<span class=\"plainlinks\">[" + y)
            else:
                to_write += ("<br />\n<span class=\"plainlinks\">[" + y)

        to_write += "\n<br />\ndrmf_eof\n\n"
        if sflag2:
            to_write += "\n"
        result += to_write

    return result
