# Version 14: Templates
# Convert tex to wikiText
import csv  # imported for using csv format
import sys  # imported for getting args
import os  # imported for copying file


def isnumber(char):
    return char[0] in "0123456789"


def getString(line):  # Gets all data within curly braces on a line
    # -------Initialization-------
    stringWrite = ""
    getStr = False
    pW = ""
    # ----------------------------
    for c in line:
        if c == "{" or c == "}":  # if there is a curly brace in the line
            getStr = not (getStr)  # toggle the getStr flag
            if c == "}":  # no more info needed
                break
        elif getStr:  # if within curly braces
            if not (pW == c and c == "-"):  # if there is no double dash (makes single dash)
                if c != "$":  # if not a $ sign
                    stringWrite += c  # this character is part of the data
                else:  # replace $ with ''
                    stringWrite += "\'\'"  # add double '
            pW = c  # change last character for finding double dashes
    return (stringWrite.rstrip('\n').lstrip())  # return the data without newlines and without leading spaces


def getG(line):  # gets equation for symbols list
    start = True
    final = ""
    for c in line:
        if c == "$" and start:
            final += "<math>{\\displaystyle "
            start = False
        elif c == "$":
            final += "}</math>"
            start = True
        else:
            final += c
    return (final)


def getEq(line):  # Gets all data within constraints,substitutions
    # -------Initialization-------
    per = 1
    stringWrite = ""
    fEq = False
    count = 0
    # ----------------------------
    for c in line:  # read each character
        if count >= 0 and per != 0:
            per += 1
            if c != " " and c != "%":
                per = 0
        if c == "{" and per == 0:
            if count > 0:
                stringWrite += c
            count += 1
        elif c == "}" and per == 0:
            count -= 1
            if count > 0:
                stringWrite += c
        elif c == "$" and per == 0:  # either begin or end equation
            fEq = not (fEq)  # toggle fEq flag to know if begin or end equation
            if fEq:  # if begin
                stringWrite += "<math>{\\displaystyle "
            else:  # if end
                stringWrite += "}</math>"
        elif c == "\n" and per == 0:  # if newline
            stringWrite = stringWrite.strip()  # remove all leading and trailing whitespace

            # should above be rstrip?<-------------------------------------------------------------------CHECK THIS

            stringWrite += c  # add the newline character
            per += 1  # watch for % signs
        elif count > 0 and per == 0:  # not special character
            stringWrite += c  # write the character

    return (stringWrite.rstrip().lstrip())


def getEqP(line, Flag):  # Gets all data within proofs
    if Flag:
        a = 1
    else:
        a = 0
    per = 1
    stringWrite = ""
    fEq = False
    count = 0
    length = 0
    for c in line:
        if fEq and c != " " and c != "$" and c != "{" and c != "}" and not c.isalpha():
            length += 1
        if count >= 0 and per != 0:
            per += 1
            if c != " " and c != "%":
                # if c!="%":
                per = 0
        if c == "{" and per == 0:
            if count > 0:
                stringWrite += c
            count += 1
        elif c == "}" and per == 0:
            count -= 1
            if count > 0:
                stringWrite += c
        elif c == "$" and per == 0:
            fEq = not (fEq)
            if fEq:
                stringWrite += "<math>{\\displaystyle "
            else:
                if length < 10:
                    stringWrite += "}</math>"
                else:
                    stringWrite += "}</math>" + "<br />"
                length = 0
        elif c == "\n" and per == 0:
            stringWrite = stringWrite.strip()
            stringWrite += c
            per += 1
        elif count > 0 and per == 0:
            stringWrite += c

    return (stringWrite.lstrip())


def getSym(line):  # Gets all symbols on a line for symbols list
    symList = []
    if line == "":
        return symList
    symbol = ""
    symFlag = False
    argFlag = False
    cC = 0
    for i in range(0, len(line)):
        # if "MeixnerPollaczek{\\lambda}{n}@{x}{\\phi}=\frac{\\pochhammer{2\\lambda}{n}}" in line:
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
                    # if "monicAskeyWilson{n+1}@{x}{a}{b}{c}{d}{q}+\\frac{1}{2}" in line:
                    symList.append(symbol)
                    symList += (getSym(symbol))
                    argFlag = False
                    symbol = ""

        elif c == "\\":
            symFlag = True
        elif c == "&":
            symList.append("&")

    # if "MeixnerPollaczek{\\lambda}{n}@{x}{\\phi}=\frac{\\pochhammer{2\\lambda}{n}}" in line:
    symList.append(symbol)
    symList += getSym(symbol)
    return (symList)


def unmodLabel(label):
    label = label.replace(".0", ".")
    label = label.replace(":0", ":")
    return (label)


def secLabel(label):
    return (label.replace("\'\'", ""))


def modLabel(label):
    # label.replace("Formula:KLS:","KLS;")
    isNumer = False
    newlabel = ""
    num = ""
    for i in range(0, len(label)):
        if isNumer and not isnumber(label[i]):
            if len(num) > 1:
                newlabel += num
                isNumer = False
                num = ""
            else:
                newlabel += "0" + str(num)
                num = ""
                isNumer = False
        if isnumber(label[i]):
            isNumer = True
            num += str(label[i])
        else:
            isNumer = False
            newlabel += label[i]
    if len(num) > 1:
        newlabel += num
    elif len(num) == 1:
        newlabel += "0" + num
    return (newlabel)


# try:
for jsahlfkjsd in range(0, 1):
    tex = open(sys.argv[1], 'r')
    wiki = open(sys.argv[2], 'w')
    main = open("OrthogonalPolynomials.mmd", "r")
    mainText = main.read()
    mainPrepend = ""
    mainWrite = open("OrthogonalPolynomials.mmd.new", "w")
    tester = open("testData.txt", 'w')
    # glossary=open('Glossary', 'r')
    glossary = open('new.Glossary.csv', 'rb')
    gCSV = csv.reader(glossary, delimiter=',', quotechar='\"')
    # lLinks=open('BruceLabelLinks', 'r')
    lGlos = glossary.readlines()
    # lLink=lLinks.readlines()
    math = False
    constraint = False
    substitution = False
    symbols = []
    lines = tex.readlines()
    refLines = []
    sections = []
    labels = []
    eqs = []
    refEqs = []
    parse = False
    head = False
    # chapRef=[("GA",open("GA.tex",'r')),("ZE",open("ZE.3.tex",'r'))]
    refLabels = []
    '''for c in chapRef:
       refLines=refLines+(c[1].readlines())
       c[1].close()'''
    for i in range(0, len(refLines)):
        line = refLines[i]
        if "\\begin{equation}" in line:
            sLabel = line.find("\\formula{") + 9
            eLabel = line.find("}", sLabel)
            label = modLabel(line[sLabel:eLabel])
            '''for l in lLink:
                   if l.find(label)!=-1 and l[len(label)+1]=="=":
                         rlabel=l[l.find("=>")+3:l.find("\\n")]
                         rlabel=rlabel.replace("/","")
                         rlabel=rlabel.replace("#",":")
                         break'''
            refLabels.append(label)
            refEqs.append("")
            math = True
        elif math:
            refEqs[len(refEqs) - 1] += line
            if "\\end{equation}" in refLines[i + 1] or "\\constraint" in refLines[i + 1] or "\\substitution" in \
                    refLines[i + 1] or "\\drmfn" in refLines[i + 1]:
                math = False

    for i in range(0, len(lines)):
        line = lines[i]
        if "\\begin{document}" in line:
            # wiki.write("drmf_bof\n")
            parse = True
        elif "\\end{document}" in line and parse:
            # wiki.write("</div>\n")
            mainPrepend += "</div>\n"
            mainText = mainPrepend + mainText
            mainText = mainText.replace("drmf_bof\n", "")
            mainText = mainText.replace("drmf_eof\n", "")
            mainText = mainText.replace("\'\'\'Orthogonal Polynomials\'\'\'\n", "")
            mainText = mainText.replace("{{#set:Section=0}}\n", "")
            mainText = mainText[0:mainText.rfind("== Sections ")]
            mainText = "drmf_bof\n\'\'\'Orthogonal Polynomials\'\'\'\n{{#set:Section=0}}\n" + mainText + "\ndrmf_eof\n"
            mainWrite.write(mainText)
            mainWrite.close()
            main.close()
            os.system("cp -f OrthogonalPolynomials.mmd.new OrthogonalPolynomials.mmd")
            # wiki.write("\ndrmf_eof\n")
            parse = False
        elif "\\title" in line and parse:
            stringWrite = "\'\'\'"
            stringWrite += getString(line) + "\'\'\'\n"
            labels.append("Orthogonal Polynomials")
            sections.append(["Orthogonal Polynomials", 0])
            # wiki.write(stringWrite)
            # mainPrepend+=stringWrite
            chapter = getString(line)
            mainPrepend += (
            "\n== Sections in " + chapter + " ==\n\n<div style=\"-moz-column-count:2; column-count:2;\">\n")
        elif "\\part" in line:
            if getString(line) == "BOF":
                parse = False
            elif getString(line) == "EOF":
                parse = True
            elif parse:
                mainPrepend += ("\n<br />\n= " + getString(line) + " =\n")
                head = True
        elif "\\section" in line:
            mainPrepend += ("* [[" + secLabel(getString(line)) + "|" + getString(line) + "]]\n")
            sections.append([getString(line)])

    secCounter = 0
    eqCounter = 0
    for i in range(0, len(lines)):
        line = lines[i]
        # line.replace("\\begin{equation}","$")
        # line.replace("\\end{equation},"$")
        '''if "\\begin{document}" in line:
              wiki.write("drmf_bof\n")
              parse=True
        elif "\\end{document}" in line and parse:
              wiki.write("\ndrmf_eof\n")
              parse=False
        elif "\\title" in line and parse:
              stringWrite="\'\'\'"
              stringWrite+=getString(line)+"\'\'\'\n"
              labels.append("Orthogonal Polynomials")
                wiki.write(stringWrite\n)
        elif "\\part" in line:
              if getString(line)=="BOF":
                     parse=False
              elif getString(line)=="EOF":
                     parse=True
              elif parse:
                     wiki.write("\n<br />\n= "+getString(line)+" =\n")
                     head=True
        '''
        if "\\section" in line:
            parse = True
            secCounter += 1
            wiki.write("drmf_bof\n")
            wiki.write("\'\'\'" + secLabel(getString(line)) + "\'\'\'\n")
            wiki.write("{{DISPLAYTITLE:" + (sections[secCounter][0]) + "}}\n")
            # wiki.write("<div id=\"drmf_head\">\n")
            # wiki.write("<div id=\"alignleft\"> << [["+secLabel(sections[secCounter-1][0])+"|"+secLabel(sections[secCounter-1][0])+"]] </div>\n")
            # wiki.write("<div id=\"aligncenter\"> [[Orthogonal_Polynomials#"+secLabel(sections[secCounter][0])+"|"+secLabel(sections[secCounter][0])+"]] </div>\n")
            # wiki.write("<div id=\"alignright\"> [["+secLabel(sections[(secCounter+1)%len(sections)][0])+"|"+secLabel(sections[(secCounter+1)%len(sections)][0])+"]] >> </div>\n</div>\n\n")
            # wiki.write("{{head|pre="+secLabel(sections[secCounter-1][0])+"|cur="+secLabel(sections[secCounter][0])+"|next="+secLabel(sections[(secCounter+1)%len(sections)][0])+"}}\n")
            wiki.write("{{#set:Chapter=" + chapter + "}}\n")
            wiki.write("{{#set:Section=" + str(secCounter) + "}}\n")
            wiki.write("{{headSection}}\n")
            head = True
            wiki.write("== " + getString(line) + " ==\n")
        elif ("\\section" in lines[(i + 1) % len(lines)] or "\\end{document}" in lines[(i + 1) % len(lines)]) and parse:
            # wiki.write("<div id=\"drmf_foot\">\n")
            # wiki.write("<div id=\"alignleft\"> << [["+secLabel(sections[secCounter-1][0])+"|"+secLabel(sections[secCounter-1][0])+"]] </div>\n")
            # wiki.write("<div id=\"aligncenter\"> [[Orthogonal_Polynomials#"+secLabel(sections[secCounter][0])+"|"+secLabel(sections[secCounter][0])+"]] </div>\n")
            # wiki.write("<div id=\"alignright\"> [["+secLabel(sections[(secCounter+1)%len(sections)][0])+"|"+secLabel(sections[(secCounter+1)%len(sections)][0])+"]] >> </div>\n</div>\n\n")
            # wiki.write("{{foot|pre="+secLabel(sections[secCounter-1][0])+"|cur="+secLabel(sections[secCounter][0])+"|next="+secLabel(sections[(secCounter+1)%len(sections)][0])+"}}\n")
            wiki.write("{{footSection}}\n")
            wiki.write("drmf_eof\n")
            sections[secCounter].append(eqCounter)
            eqCounter = 0

        elif "\\subsection" in line and parse:
            wiki.write("\n== " + getString(line) + " ==\n")
            head = True
        elif "\\paragraph" in line and parse:
            wiki.write("\n=== " + getString(line) + " ===\n")
            head = True
        elif "\\subsubsection" in line and parse:
            wiki.write("\n=== " + getString(line) + " ===\n")
            head = True

        elif "\\begin{equation}" in line and parse:
            #                                                                          symLine=""
            if head:
                wiki.write("\n")
                head = False
            sLabel = line.find("\\formula{") + 9
            eLabel = line.find("}", sLabel)
            label = modLabel(line[sLabel:eLabel])
            eqCounter += 1
            '''for l in lLink:
                   if label==l[0:l.find("=")-1]:
                         rlabel=l[l.find("=>")+3:l.find("\\n")]
                         rlabel=rlabel.replace("/","")
                         rlabel=rlabel.replace("#",":")
                         rlabel=rlabel.replace("!",":")
                         break'''
            labels.append(label)
            eqs.append("")
            # wiki.write("\n<span id=\""+label.lstrip("Formula:")+"\"></span>\n")
            wiki.write("<math id=\"" + label.lstrip("Formula:") + "\">{\displaystyle \n")
            math = True
        elif "\\begin{equation}" in line and not parse:
            sLabel = line.find("\\formula{") + 9
            eLabel = line.find("}", sLabel)
            label = modLabel(line[sLabel:eLabel])
            '''for l in lLink:
                   if l.find(label)!=-1:
                         rlabel=l[l.find("=>")+3:l.find("\\n")]
                         rlabel=rlabel.replace("/","")
                         rlabel=rlabel.replace("#",":")
                         break'''
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
        # wiki.write("<div align=\"right\">Substitution(s): "+getEq(line)+"</div><br />\n")
        elif "\\proof" in line and parse:
            math = False
        elif "\\drmfn" in line and parse:
            math = False
            if "\\drmfname" in line and parse:
                wiki.write("<div align=\"right\">This formula has the name: " + getString(line) + "</div><br />\n")
        elif math and parse:
            flagM = True
            eqs[len(eqs) - 1] += line

            if "\\end{equation}" in lines[i + 1] and not "\\subsection" in lines[i + 3] and not "\\section" in lines[
                        i + 3] and not "\\part" in lines[i + 3]:
                u = i
                flagM2 = False
                while flagM:
                    u += 1
                    if "\\begin{equation}" in lines[u] in lines[u]:
                        flagM = False
                    if "\\section" in lines[u] or "\\subsection" in lines[i] or "\\part" in lines[
                        u] or "\\end{document}" in lines[u]:
                        flagM = False
                        flagM2 = True
                if not (flagM2):

                    wiki.write(line.rstrip("\n"))
                    wiki.write("\n}</math><br />\n")
                else:
                    wiki.write(line.rstrip("\n"))
                    wiki.write("\n}</math>\n")
            elif "\\end{equation}" in lines[i + 1]:
                wiki.write(line.rstrip("\n"))
                wiki.write("\n}</math>\n")
            elif "\\constraint" in lines[i + 1] or "\\substitution" in lines[i + 1] or "\\drmfn" in lines[i + 1]:
                wiki.write(line.rstrip("\n"))
                wiki.write("\n}</math>\n")
            else:
                wiki.write(line)
        elif math and not parse:
            eqs[len(eqs) - 1] += line
            if "\\end{equation}" in lines[i + 1] or "\\constraint" in lines[i + 1] or "\\substitution" in lines[
                        i + 1] or "\\drmfn" in lines[i + 1]:
                math = False
        if substitution and parse:
            subLine = subLine + line.replace("&", "&<br />")
            if "\\end{equation}" in lines[i + 1] or "\\substitution" in lines[i + 1] or "\\constraint" in lines[
                        i + 1] or "\\drmfn" in lines[i + 1] or "\\proof" in lines[i + 1]:
                substitution = False
                wiki.write("<div align=\"right\">Substitution(s): " + getEq(subLine) + "</div><br />\n")

        if constraint and parse:
            conLine = conLine + line.replace("&", "&<br />")
            if "\\end{equation}" in lines[i + 1] or "\\substitution" in lines[i + 1] or "\\constraint" in lines[
                        i + 1] or "\\drmfn" in lines[i + 1] or "\\proof" in lines[i + 1]:
                constraint = False
                wiki.write("<div align=\"right\">Constraint(s): " + getEq(conLine) + "</div><br />\n")

    eqCounter = 0
    endNum = len(labels) - 1
    '''for n in range(1,len(labels)):
           if n+1!=len(labels) and labels[n+1][0]=="*" and labels[n][0]!="*":
             labels[n]=""+labels[n]
             endNum=n
           elif labels[n][0]=="*":
             labels[n]=""+labels[n][1:]
           else:
             labels[n]=""+labels[n]'''
    '''for n in range(0,len(refLabels)):
             refLabels[n]=""+refLabels[n]'''
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
            wiki.write("drmf_bof\n")
            label = labels[eqCounter]
            wiki.write("\'\'\'" + secLabel(label) + "\'\'\'\n")
            wiki.write("{{DISPLAYTITLE:" + (labels[eqCounter]) + "}}\n")
            if eqCounter < endNum:  # FOR ANYTHING THAT IS NOT THE EXTRA EQUATIONS
                wiki.write("<div id=\"drmf_head\">\n")
                if newSec:
                    wiki.write("<div id=\"alignleft\"> << [[" + secLabel(sections[secCount][0]).replace(" ",
                                                                                                        "_") + "|" + secLabel(
                        sections[secCount][0]) + "]] </div>\n")
                else:
                    wiki.write("<div id=\"alignleft\"> << [[" + secLabel(labels[eqCounter - 1]).replace(" ",
                                                                                                        "_") + "|" + secLabel(
                        labels[eqCounter - 1]) + "]] </div>\n")
                wiki.write("<div id=\"aligncenter\"> [[" + secLabel(sections[secCount + 1][0]).replace(" ",
                                                                                                       "_") + "#" + secLabel(
                    labels[eqCounter][len("Formula:"):]) + "|formula in " + secLabel(
                    sections[secCount + 1][0]) + "]] </div>\n")
                if eqS == sections[secCount][1]:
                    wiki.write(
                        "<div id=\"alignright\"> [[" + secLabel(sections[(secCount + 1) % len(sections)][0]).replace(
                            " ", "_") + "|" + secLabel(sections[(secCount + 1) % len(sections)][0]) + "]] >> </div>\n")
                else:
                    wiki.write(
                        "<div id=\"alignright\"> [[" + secLabel(labels[(eqCounter + 1) % (endNum + 1)]).replace(" ",
                                                                                                                "_") + "|" + secLabel(
                            labels[(eqCounter + 1) % (endNum + 1)]) + "]] >> </div>\n")
                wiki.write("</div>\n\n")
            elif eqCounter == endNum:
                wiki.write("<div id=\"drmf_head\">\n")
                if newSec:
                    newSec = False
                    wiki.write("<div id=\"alignleft\"> << [[" + secLabel(sections[secCount][0]).replace(" ",
                                                                                                        "_") + "|" + secLabel(
                        sections[secCount][0]) + "]] </div>\n")
                else:
                    wiki.write("<div id=\"alignleft\"> << [[" + secLabel(labels[eqCounter - 1]).replace(" ",
                                                                                                        "_") + "|" + secLabel(
                        labels[eqCounter - 1]) + "]] </div>\n")
                wiki.write("<div id=\"aligncenter\"> [[" + secLabel(sections[secCount + 1][0]).replace(" ",
                                                                                                       "_") + "#" + secLabel(
                    labels[eqCounter][len("Formula:"):]) + "|formula in " + secLabel(
                    sections[secCount + 1][0]) + "]] </div>\n")
                wiki.write("<div id=\"alignright\"> [[" + secLabel(
                    labels[(eqCounter + 1) % (endNum + 1)].replace(" ", "_")) + "|" + secLabel(
                    labels[(eqCounter + 1) % (endNum + 1)]) + "]] </div>\n")
                wiki.write("</div>\n\n")

            wiki.write("<br /><div align=\"center\"><math>{\displaystyle \n")
            math = True
        elif "\\end{equation}" in line:
            wiki.write(comToWrite)
            parse = False
            math = False
            if hProof:
                wiki.write(
                    "\n== Proof ==\n\nWe ask users to provide proof(s), reference(s) to proof(s), or further clarification on the proof(s) in this space.\n")

            wiki.write("\n== Symbols List ==\n\n")
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
            symF = False
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
                numArg = parCx
                numPar = ArgCx
                gFlag = False
                checkFlag = False
                get = False
                gCSV = csv.reader(open('new.Glossary.csv', 'rb'), delimiter=',', quotechar='\"')
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

                    if (get):
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
                        '''websiteU=g[g.find("http://"):].strip("\n")
                        k=0
                        websites=[]
                        for r in range(0,len(websiteU)):
                            if websiteU[r]==",":
                                 if websiteU[k:r].find("http://")!=-1:
                                     websites.append(websiteU[k:r+1].strip(" "))
                                     k=r


                        if websiteU[k:r].find("http://")!=-1:
                               websites.append(websiteU[k:r+1].strip(" "))
                        websiteF=""
                        for d in websites:
                               websiteF=websiteF+" ["+d+" "+d+"]"'''
                        # websiteF=G[4].strip("\n")
                        websiteF = ""
                        web1 = G[5]
                        for t in range(5, len(G)):
                            if G[t] != "":
                                websiteF = websiteF + " [" + G[t] + " " + G[t] + "]"

                                # p1=Q
                                # if Q.find("@")!=-1:
                                # p1=Q[:Q.find("@")]
                        p1 = G[4].strip("$")
                        p1 = "<math>{\\displaystyle " + p1 + "}</math>"
                        # if checkFlag:
                        new1 = ""
                        new2 = ""
                        pause = False
                        mathF = True
                        '''for k in range(0,len(p1)):
                               if p1[k]=="$":
                                     if mathF:
                                            new1+="<math>{\\displaystyle "
                                     else:
                                            new1+="}</math>"
                                     mathF=not mathF

                               elif p1[k]=="#" and p1[k+1].isdigit():
                                     pause=True
                               elif pause:
                                     num=int(p1[k])
                                     #letter=chr(num+96)
                                     letter=listArgs[num-1]
                                     new1+=letter
                                     pause=False

                               else:
                                     new1+=p1[k]'''
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
                        # p1=new1
                        p2 = new2
                        finSym.append(web1 + " " + p1 + "]</span> : " + p2 + " :" + websiteF)
                        break
                        # gFlag=True
                        # if not symF:
                    #	symF=True
                    #	wiki.write("<span class=\"plainlinks\">[")
                    # else:
                    #	wiki.write("<br />\n")
                    #	wiki.write("<span class=\"plainlinks\">[")
                    # wiki.write(g[g.find("http://"):].strip("\n"))
                    # wiki.write(" ")
                    # wiki.write(getEq(g[g.find("{$"):]).strip("\n").replace("\\\\","\\"))
                    # wiki.write("]</span> : ")
                    # wiki.write(g[g.find(" {")+2:g.find("} ",g.find(" {")+1)])
                    # wiki.write(" : [")
                    # wiki.write(g[g.find("http://"):].strip("\n"))
                    # wiki.write(" ")
                    # wiki.write(g[g.find("http://"):].strip("\n"))
                    # wiki.write("] ")'''

                # preG=S
                if not gFlag:
                    del newSym[s]

            gFlag = True
            # finSym.reverse()
            if ampFlag:
                wiki.write("& : logical and")
                gFlag = False
            for y in finSym:
                if y == "& : logical and":
                    pass
                elif gFlag:
                    gFlag = False
                    wiki.write("<span class=\"plainlinks\">[" + y)
                else:
                    wiki.write("<br />\n<span class=\"plainlinks\">[" + y)

            wiki.write("\n<br />\n")

            wiki.write("\n== Bibliography==\n\n")  # should there be a space between bibliography and ==?
            r = unmodLabel(labels[eqCounter])
            q = r.find("KLS:") + 4
            p = r.find(":", q)
            section = r[q:p]
            equation = r[p + 1:]
            if equation.find(":") != -1:
                equation = equation[0:equation.find(":")]

            wiki.write(
                "<span class=\"plainlinks\">[http://homepage.tudelft.nl/11r49/askey/contents.html Equation in Section " + section + "]</span> of [[Bibliography#KLS|'''KLS''']].\n\n")  # Where should it link to?
            wiki.write("== URL links ==\n\nWe ask users to provide relevant URL links in this space.\n\n")
            if eqCounter < endNum:
                wiki.write("<br /><div id=\"drmf_foot\">\n")
                if newSec:
                    newSec = False
                    wiki.write("<div id=\"alignleft\"> << [[" + secLabel(sections[secCount][0]).replace(" ",
                                                                                                        "_") + "|" + secLabel(
                        sections[secCount][0]) + "]] </div>\n")
                else:
                    wiki.write("<div id=\"alignleft\"> << [[" + secLabel(labels[eqCounter - 1]).replace(" ",
                                                                                                        "_") + "|" + secLabel(
                        labels[eqCounter - 1]) + "]] </div>\n")
                wiki.write("<div id=\"aligncenter\"> [[" + secLabel(sections[secCount + 1][0]).replace(" ",
                                                                                                       "_") + "#" + secLabel(
                    labels[eqCounter][len("Formula:"):]) + "|formula in " + secLabel(
                    sections[secCount + 1][0]) + "]] </div>\n")
                if eqS == sections[secCount][1]:
                    wiki.write("<div id=\"alignright\"> [[" + sections[(secCount + 1) % len(sections)][0].replace(" ",
                                                                                                                  "_") + "|" +
                               sections[(secCount + 1) % len(sections)][0] + "]] >> </div>\n")
                else:
                    wiki.write(
                        "<div id=\"alignright\"> [[" + secLabel(labels[(eqCounter + 1) % (endNum + 1)]).replace(" ",
                                                                                                                "_") + "|" + secLabel(
                            labels[(eqCounter + 1) % (endNum + 1)]) + "]] >> </div>\n")
                wiki.write("</div>\n\ndrmf_eof\n")
            else:  # FOR EXTRA EQUATIONS
                wiki.write("<br /><div id=\"drmf_foot\">\n")
                wiki.write("<div id=\"alignleft\"> << [[" + labels[endNum - 1].replace(" ", "_") + "|" + labels[
                    endNum - 1] + "]] </div>\n")
                wiki.write("<div id=\"aligncenter\"> [[" + labels[0].replace(" ", "_") + "#" + labels[endNum][
                                                                                               8:] + "|formula in " +
                           labels[0] + "]] </div>\n")
                wiki.write("<div id=\"alignright\"> [[" + labels[(0) % endNum].replace(" ", "_") + "|" + labels[
                    0 % endNum] + "]] </div>\n")
                wiki.write("</div>\n\ndrmf_eof\n")



        elif "\\constraint" in line and parse:
            # symbols=symbols+getSym(line)
            symLine = line.strip("\n")
            if hCon:
                comToWrite = comToWrite + "\n== Constraint(s) ==\n\n"
                hCon = False
                constraint = True
                math = False
                conLine = ""
            # wiki.write("<div align=\"left\">"+getEq(line)+"</div><br />\n")
        elif "\\substitution" in line and parse:
            # symbols=symbols+getSym(line)
            symLine = line.strip("\n")
            if hSub:
                comToWrite = comToWrite + "\n== Substitution(s) ==\n\n"
                hSub = False
            # wiki.write("<div align=\"left\">"+getEq(line)+"</div><br />\n")
            substitution = True
            math = False
            subLine = ""
        elif "\\drmfname" in line and parse:
            math = False
            comToWrite = "\n== Name ==\n\n<div align=\"left\">" + getString(line) + "</div><br />\n" + comToWrite

        elif "\\drmfnote" in line and parse:
            symbols = symbols + getSym(line)
            if hNote:
                comToWrite = comToWrite + "\n== Note(s) ==\n\n"
                hNote = False
            note = True
            math = False
            noteLine = ""

        elif "\\proof" in line and parse:
            # symbols=symbols+getSym(line)
            symLine = line.strip("\n")
            if hProof:
                hProof = False
                comToWrite = comToWrite + "\n== Proof ==\n\nWe ask users to provide proof(s), reference(s) to proof(s), or further clarification on the proof(s) in this space. \n<br /><br />\n<div align=\"left\">"
            proof = True
            proofLine = ""
            pause = False
            pauseP = False
            for ind in range(0, len(line)):
                if line[ind:ind + 7] == "\\eqref{":
                    pause = True
                    eqR = line[ind:line.find("}", ind) + 1]
                    rLab = getString(eqR)
                    '''for l in lLink:
                                       if rLab==l[0:l.find("=")-1]:
                                           rlabel=l[l.find("=>")+3:l.find("\\n")]
                                             rlabel=rlabel.replace("/","")
                                           rlabel=rlabel.replace("#",":")
                                           rlabel=rlabel.replace("!",":")
                                              break'''

                    eInd = refLabels.index("" + label)
                    z = line[line.find("}", ind + 7) + 1]
                    if z == "." or z == ",":
                        pauseP = True
                        proofLine += ("<br /> \n<math id=\"" + label + "\">{\displaystyle \n" + refEqs[
                            eInd] + "}</math>" + z + "<br />\n")
                    else:
                        if z == "}":
                            proofLine += (
                            "<br /> \n<math id=\"" + label + "\">{\displaystyle \n" + refEqs[eInd] + "}</math><br />")
                        else:
                            proofLine += (
                            "<br /> \n<math id=\"" + label + "\">{\displaystyle \n" + refEqs[eInd] + "}</math><br />\n")


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
                # symLine+=line.strip("\n")
                wiki.write(comToWrite + getEqP(proofLine, False) + "</div>\n<br />\n")
                comToWrite = ""
                symbols = symbols + getSym(symLine)
                symLine = ""

            # wiki.write(line)

        elif proof:
            symLine += line.strip("\n")
            pauseP = False
            # symbols=symbols+getSym(line)
            for ind in range(0, len(line)):
                if line[ind:ind + 7] == "\\eqref{":
                    pause = True
                    eqR = line[ind:line.find("}", ind) + 1]
                    rLab = getString(eqR)
                    '''for l in lLink:
                                       if rLab==l[0:l.find("=")-1]:
                                           rlabel=l[l.find("=>")+3:l.find("\\n")]
                                             rlabel=rlabel.replace("/","")
                                           rlabel=rlabel.replace("#",":")
                                           rlabel=rlabel.replace("!",":")
                                              break'''

                    eInd = refLabels.index("" + label)
                    z = line[line.find("}", ind + 7) + 1]
                    if z == "." or z == ",":
                        pauseP = True
                        proofLine += ("<br /> \n<math id=\"" + label + "\">{\displaystyle \n" + refEqs[
                            eInd] + "}</math>" + z + "<br />\n")
                    else:
                        proofLine += (
                        "<br /> \n<math id=\"" + label + "\">{\displaystyle \n" + refEqs[eInd] + "}</math><br />\n")

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
                # symLine+=line.strip("\n")
                wiki.write(comToWrite + getEqP(proofLine, False).rstrip("\n") + "</div>\n<br />\n")
                comToWrite = ""
                symbols = symbols + getSym(symLine)
                symLine = ""

        elif math:
            if "\\end{equation}" in lines[i + 1] or "\\constraint" in lines[i + 1] or "\\substitution" in lines[
                        i + 1] or "\\proof" in lines[i + 1] or "\\drmfnote" in lines[i + 1] or "\\drmfname" in lines[
                        i + 1]:
                wiki.write(line.rstrip("\n"))
                symLine += line.strip("\n")
                symbols = symbols + getSym(symLine)
                symLine = ""
                wiki.write("\n}</math></div>\n")
            else:
                symLine += line.strip("\n")
                wiki.write(line)
        if note and parse:
            noteLine = noteLine + line
            symbols = symbols + getSym(line)
            if "\\end{equation}" in lines[i + 1] or "\\drmfn" in lines[i + 1] or "\\constraint" in lines[
                        i + 1] or "\\substitution" in lines[i + 1] or "\\proof" in lines[i + 1]:
                note = False
                comToWrite = comToWrite + "<div align=\"left\">" + getEq(noteLine) + "</div><br />\n"

        if constraint and parse:
            conLine = conLine + line.replace("&", "&<br />")

            symLine += line.strip("\n")
            # symbols=symbols+getSym(line)
            if "\\end{equation}" in lines[i + 1] or "\\drmfn" in lines[i + 1] or "\\constraint" in lines[
                        i + 1] or "\\substitution" in lines[i + 1] or "\\proof" in lines[i + 1]:
                constraint = False
                symbols = symbols + getSym(symLine)
                symLine = ""
                wiki.write(comToWrite + "<div align=\"left\">" + getEq(conLine) + "</div><br />\n")
                comToWrite = ""
        if substitution and parse:
            subLine = subLine + line.replace("&", "&<br />")

            symLine += line.strip("\n")
            # symbols=symbols+getSym(line)
            if "\\end{equation}" in lines[i + 1] or "\\drmfn" in lines[i + 1] or "\\substitution" in lines[
                        i + 1] or "\\constraint" in lines[i + 1] or "\\proof" in lines[i + 1]:
                substitution = False
                symbols = symbols + getSym(symLine)
                symLine = ""
                wiki.write(comToWrite + "<div align=\"left\">" + getEq(subLine) + "</div><br />\n")
                comToWrite = ""
# except Exception as detail: #If exception occured
#	   print("Exception",detail) #print details of error
# except: #If anythin else occured...
#	 print ("ERROR",sys.exc_info()[0])#ERROR with basic info
