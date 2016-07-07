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
        # if "MeixnerPollaczek{\\lambda}{n}@{x}{\\phi}=\frac{\\pochhammer{2\\lambda}{n}}" in line:
        #	print symbol
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
                    # print(symbol,p)
                    symList.append(symbol)
                    # if symbol=="binom{n}{k}":print line
                    symList += (getSym(symbol))
                    argFlag = False
                    symbol = ""

        elif c == "\\":
            symFlag = True

        # if "MeixnerPollaczek{\\lambda}{n}@{x}{\\phi}=\frac{\\pochhammer{2\\lambda}{n}}" in line:
        # print symbol
    symList.append(symbol)
    # if "ctsbigqHermite" in line:
    # print(symList)
    symList += getSym(symbol)
    return (symList)


import csv

# files_in_dir=os.listdir(".")
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
        # t+=T[0]+T[1]
        # print T[n]
        # t=t[t.find("<br />"):]+t[0:t.find("<br />")]
        t = t.replace("\n", " ")
        # if "Symbol" in t:print t
        symbols = getSym(t)
        # print symbols
        # if "qsin" in g:print t,symbols
        # if "Neumann" in g:print t,"\n",symbols
        if True:
            toWrite += ("== Symbols List ==\n\n")
            newSym = []
            # if "09.07:04" in label:
            # print(symbols)
            for x in symbols:
                flagA = True
                # if x not in newSym:
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

                    if y[:cN].strip() == noA.strip():  # and ArgC==ArgCx:
                        flagA = False
                        # print(x,y)
                        break
                if flagA:
                    newSym.append(x)
            newSym.reverse()
            # print newSym
            # if "14.27:02" in label:
            # print newSym
            symF = False
            finSym = []
            for s in range(len(newSym) - 1, -1, -1):
                # print(newSym[s])
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
                    # if "14.27:02" in label:print symbolPar,symbol
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
                        len(symbol)].isalpha()):  # and (numPar!=0 or numArg!=0):
                        checkFlag = True
                        get = True
                        preG = S
                    # if "14.27:02" in label:print "ok" + symbol

                    # if "9.07:04" in label:print symbol,numPar,numArg,parCx,ArgCx

                    elif checkFlag:
                        get = True
                        checkFlag = False
                    if (get):
                        if get:
                            G = preG
                        # print preG
                        get = False
                        checkFlag = False
                        # if "14.27:02" in label:print "yes"+symbol
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
                        # print("(",G,")")
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
                        # print(p1)
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
            for y in finSym:
                # print(finSym)
                if gFlag:
                    gFlag = False
                    toWrite += ("<span class=\"plainlinks\">[" + y)
                else:
                    toWrite += ("<br />\n<span class=\"plainlinks\">[" + y)

            toWrite += ("\n<br />\ndrmf_eof\n\n")
            if sflag2:
                toWrite += "\n"
            main.write(toWrite)
