import os
import time

localtime = time.asctime(time.localtime(time.time())).replace(" ", "_")
os.system("cp main_page.mmd main_page.mmd" + str(localtime))


def compString(a, b):
    x = a[0:a.find("|")]
    y = b[0:b.find("|")]
    if len(x) > len(y):
        max = len(y)
        ret = False
    else:
        max = len(x)
        ret = True
    if True:
        for i in range(0, max):
            if ord(x[i].lower()) < ord(y[i].lower()):
                return True
            elif ord(x[i].lower()) > ord(y[i].lower()):
                return False
    return ret


def sumOrd(x):
    sum = 0
    for s in x:
        sum += ord(s)
    return (sum)


def sort(x):
    ret = []
    ret.append(x[0])
    for i in range(1, len(x)):
        if compString(x[i], ret[0]):
            ret = [x[i]] + ret
        elif compString(ret[len(ret) - 1], x[i]):
            ret.append(x[i])
        else:
            for p in range(1, len(ret)):
                if compString(x[i], ret[p]):
                    ret = ret[0:p] + [x[i]] + ret[p:]
                    break
    return (ret)


'''listFile=open("list.txt","w")
files_in_dir=os.listdir(".")
toWrite=[]
for g in files_in_dir:
	   if ".new" in g and "Definition:" in g:
			 g=g[:g.find(".new")]
			 element="* [["+g+"|"+g[len("Definition:"):]+"]]"
			 toWrite.append(element)
			 toWrite=sort(toWrite)
text=""
for g in toWrite:
	   text+=(g+"\n")
listFile.close()
listFile=open("list.txt","r")
text=listFile.read()'''
main = open("main_page.mmd", "r")
mainText = main.read()
mainLines = mainText.split("\n")
main.close()
toWrite = []
for z in mainLines:
    if "\'\'\'Definition:" in z:
        g = z[z.find("\'\'\'Definition:") + len("\'\'\'"):z.find("\'\'\'", z.find("\'\'\'Definition:") + 4)]
        element = "* [[" + g + "|" + g[len("Definition:"):] + "]]"
        toWrite.append(element)
main = open("main_page.mmd", "w")
s = mainText.find("== Definition Pages ==")
e = mainText.find("= Copyright =")
text = ""
for g in toWrite:
    text += (g + "\n")
# print text
# print mainText[:s]
newText = mainText[
          :s] + "== Definition Pages ==\n\n<div style=\"-moz-column-count:2; column-count:2;-webkit-column-count:2\">\n" + text + "</div>\n\n" + mainText[
                                                                                                                                                 e:]
main.write(newText)
main.close()
