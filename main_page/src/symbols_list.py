__author__ = "Azeem Mohammed"
__status__ = "Development"

import csv


def getSym(line):  # Gets all symbols on a line for symbols list
    line = line.replace("\n", " ")
    symList = []
    if line == "":
        return symList
    symbol = ""
    symFlag = False
    argFlag = False
    cC = 0
    for i in range(0, len(line)):
        c = line[i]
        if symFlag:
            if c == "{" or c == "[":
                cC += 1
                argFlag = True
            if c != "}" and c != "]":
                if argFlag or c.isalpha():
                    symbol += c
                else:
                    symFlag = False
                    argFlag = False
                    symList.append(symbol)
                    symList += (getSym(symbol))
                    symbol = ""
            else:
                cC -= 1
                symbol += c
                if i + 1 == len(line):
                    p = ""
                else:
                    p = line[i + 1]
                if cC == 0 and p != "{" and p != "[" and p != "@":
                    symFlag = False
                    symList.append(symbol)
                    symList += (getSym(symbol))
                    argFlag = False
                    symbol = ""

        elif c == "\\":
            symFlag = True

    symList.append(symbol)
    symList += getSym(symbol)
    return symList

mainPage = open("main_page.mmd", "r")
mainLines = mainPage.read()
mainLines = mainLines[mainLines.find("drmf_bof"):mainLines.rfind("drmf_eof") + len("drmf_eof\n")]
mainPage.close()
main = open("main_page.mmd", "w")
mainPages = mainLines.split("drmf_eof")

if mainPages[-1].strip() == "":
    mainPages = mainPages[0:len(mainPages) - 1]

print len(mainPages)

glossary = open('new.Glossary.csv', 'rb')
gCSV = csv.reader(glossary, delimiter=',', quotechar='\"')
lGlos = glossary.readlines()
wiki = ""

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
        sflag1 = False
        sflag2 = False
        if h.find("== Symbols List ==") != -1:
            toWrite = h[0:h.find("== Symbols List ==")]
            h = toWrite
        else:
            sflag1 = True
            if h.find("drmf_foot") == -1:
                toWrite = h
                sflag2 = True
            else:
                toWrite = h[0:h.find("<div id=\"drmf_foot")]
                h = toWrite
        toWrite = "drmf_bof\n" + toWrite
        toWrite.strip("\n")
        if sflag1:
            toWrite += "\n\n"
        T = h.split("\n")
        n = 0
        '''for q in T:
            if "These are defined by" in q:
               break
           n+=1'''
        t = ""
        for p in range(n, len(T)):
            t += T[p] + " "
        t = t.replace("\n", " ")
        symbols = getSym(t)
        if True:
            toWrite += ("== Symbols List ==\n\n")
            newSym = []
            for x in symbols:
                flagA = True
                cN = 0
                cC = 0
                flag = True
                ArgCx = 0
                for z in x:
                    if z.isalpha() and flag:
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
                        if z.isalpha() and flag:
                            cN += 1
                        else:
                            flag = False
                            if z == "{" or z == "[":
                                cC += 1
                            if z == "}" or z == "]":
                                cC -= 1
                                if cC == 0:
                                    ArgC += 1

                    if y[:cN].strip() == noA.strip():
                        flagA = False
                        break
                if flagA:
                    newSym.append(x)
            newSym.reverse()
            symF = False
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

                if symbolPar.find("{") != -1 or symbolPar.find("[") != -1:
                    if symbolPar.find("[") == -1:
                        symbol = symbolPar[0:symbolPar.find("{")]
                    elif symbolPar.find("{") == -1 or symbolPar.find("[") < symbolPar.find("{"):
                        symbol = symbolPar[0:symbolPar.find("[")]
                    else:
                        symbol = symbolPar[0:symbolPar.find("{")]
                else:
                    symbol = symbolPar
                numArg = parCx
                numPar = ArgCx
                gFlag = False
                checkFlag = False
                get = False
                gCSV = csv.reader(open('new.Glossary.csv', 'rb'), delimiter=',', quotechar='\"')
                preG = ""
                symbol = symbol.strip("}").strip("]")
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
                        len(symbol)].isalpha()):
                        checkFlag = True
                        get = True
                        preG = S
                    elif checkFlag:
                        get = True
                        checkFlag = False

                    if get:
                        if get:
                            G = preG
                        get = False
                        checkFlag = False
                        if True:
                            if symbolPar.find("@") != -1:
                                Q = symbolPar[:symbolPar.find("@")]
                            else:
                                Q = symbolPar
                        listArgs = []
                        if len(Q) > len(symbol) and (Q[len(symbol)] == "{" or Q[len(symbol)] == "["):
                            ap = ""
                            for o in range(len(symbol), len(Q)):
                                if Q[o] == "{" or z == "[":
                                    argFlag = True
                                elif Q[o] == "}" or z == "]":
                                    argFlag = False
                                    listArgs.append(ap)
                                    ap = ""
                                else:
                                    ap += Q[o]
                        websiteF = ""
                        web1 = G[5]
                        for t in range(5, len(G)):
                            if G[t] != "":
                                websiteF = websiteF + " [" + G[t] + " " + G[t] + "]"
                        p1 = G[4].strip("$")
                        p1 = "<math>{\\displaystyle " + p1 + "}</math>"
                        new1 = ""
                        new2 = ""
                        pause = False
                        mathF = True
                        p2 = G[1]
                        for k in range(0, len(p2)):
                            if p2[k] == "$":
                                if mathF:
                                    new2 += "<math>{\\displaystyle "
                                else:
                                    new2 += "}</math>"
                                mathF = not mathF
                            else:
                                new2 += p2[k]
                        p2 = new2
                        finSym.append(web1 + " " + p1 + "]</span> : " + p2 + " :" + websiteF)
                        break
                if not gFlag:
                    del newSym[s]

            gFlag = True
            for y in finSym:
                if gFlag:
                    gFlag = False
                    toWrite += ("<span class=\"plainlinks\">[" + y)
                else:
                    toWrite += ("<br />\n<span class=\"plainlinks\">[" + y)

            toWrite += "\n<br />\ndrmf_eof\n\n"
            if sflag2:
                toWrite += "\n"
            main.write(toWrite)
