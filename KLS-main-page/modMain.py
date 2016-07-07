file = open("main_page.mmd", "r")
import csv

lines = file.read()
lines = lines.replace("The LaTeX DLMF macro \'\'\'\\", "The LaTeX DLMF and DRMF macro \'\'\'\\")
file.close()
file = open("main_page.mmd", "w")
flag = True
gCSV = csv.reader(open('new.Glossary.csv', 'rb'), delimiter=',', quotechar='\"')
toWrite = ""
i = 0


def atSort(l):
    return (sorted(l, key=lambda x: x.count("@")))


def remOpt(p):
    parse = True
    ret = ""
    for x in p:
        if parse:
            if x == "[":
                parse = False
            else:
                ret += x
        else:
            if x == "]":
                parse = True
    return ret


def findAllPos(g):
    key = g[3]
    orig = g[0]
    r = key[:key.find("|")]
    key = key[key.find("|") + 1:]
    keys = key.split(":")
    ret = []
    for x in keys:
        if x == "F" or x == "FO" or x == "O" or x == "O1":
            if orig.find("@") != -1:
                ret.append(orig[0:orig.find("@")])
                if x == "O":
                    ret.append(orig)
            else:
                ret.append(orig)
        if x == "FnO":  # remove optional parameters
            if orig.find("@") != -1:
                ret.append(remOpt(orig[0:orig.find("@")]))
            else:
                ret.append(remOpt(orig))
        if x == "P" or x == "PO":
            ret.append(orig.replace("@@", "@"))
        if x == "PnO":  # remove optional parameters
            ret.append(remOpt(orig.replace("@@", "@")))
        if x == "nP" or x == "nPO" or x == "PS" or x == "O2":
            ret.append(orig)
        if x == "nPnO":  # remove optional paramters
            ret.append(remOpt(orig))
        if "fo" in x:
            ret.append(orig.replace("@@@", "@" * int(x[2])))
    return atSort(ret), r


categories = open("Categories.txt", "r")
cats = categories.readlines()
categories.close()
for x in range(0, len(cats)):
    cats[x] = cats[x].strip()
while flag:
    n = lines.find("\'\'\'Definition:", i)
    if n == -1:
        flag = False
        # elif lines.find("This macro can be called in the following way")<lines.find("\'\'\'Definition:",n+len("\'\'\'Definition:")+1):
        # Update it
    else:
        macroN = lines[n + len("\'\'\'Definition:"):lines.find("\'\'\'", n + len("\'\'\'Definition:"))]
        r = lines.find("\'\'\'\\", n)
        q = lines.find("\'\'\'", r + len("\'\'\'\\"))
        if lines[r:q].find("{") != -1:
            lines = lines[0:r] + "\'\'\'\\" + macroN + lines[q:]

        if lines.find("\nThis macro is in the category of", n) < lines.find("\'\'\'Definition:", n + len(
                "\'\'\'Definition:") + 1) and lines.find("\nThis macro is in the category of", n) != -1:
            # print n
            p = lines.find("\nThis macro is in the category of", n)
        else:
            p = lines.find("\n", lines.find(".", n))
        toWrite += lines[i:p]
        toWrite = toWrite.rstrip()
        toWrite += "\n\n"
        count = 0
        listCalls = []
        gCSV = csv.reader(open('new.Glossary.csv', 'rb'), delimiter=',', quotechar='\"')
        for g in gCSV:
            if g[0].find("\\" + macroN) == 0 and (len(g[0]) == len(macroN) + 1 or not g[0][len(macroN) + 1].isalpha()):
                # count+=1
                # listCalls.append(g[0])
                q, s = findAllPos(g)
                listCalls += q
                count += len(q)
        # count= number of entries for the macro
        plural = 1  # if count>1: plural =1; if count=1: plural=0
        if count == 1: plural = 0
        for t in cats:
            if s + "    -" in t:
                category = "This macro is in the category of" + t[t.find("-") + 2:]
                break
        new = category + "\n\nIn math mode, this macro can be called in the following way" + "s" * plural + ":\n\n"
        for q in range(0, len(listCalls)):
            c = listCalls[q]
            new += ":\'\'\'" + c + "\'\'\'" + " produces <math>{\\displaystyle " + c + "}</math><br />\n"
        # Now add the multiple ways \macroname{n}@... produces <math>\macroname{n}@...</math>
        toWrite += new + "\n"
        i = lines.find("These are defined by", p)
file.write(toWrite + lines[i:])
