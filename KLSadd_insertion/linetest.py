"""
TODO: Rewrite the whole thing so another human being can read it
jeez this is like my handwriting; it's nonsense to everyone but me
This started out as a test file but I just kept writing it 
and writing it
and writing it
and now its the project
"""

entireFile = ""
subsections = []
index = 0
headings = []
sections = []
mathPeople = []
newCommands = []
#can you tell I like lists?
name = ""
temp = "" 
with open("KLSadd.tex", "r") as file:
        entireFile = file.readlines()
        for word in entireFile:
                index+=1
                if("smallskipamount" in word):
                        newCommands.append(index-1)
                if("mybibitem[1]" in word):
                        newCommands.append(index)
                #1/27/16 RS added \large\bf KLSadd: to make KLSadd additions appear like the other paragraphs
                if("paragraph{" in word):
                        temp = word[0:word.find("{")+ 1] + "\large\\bf KLSadd: " + word[word.find("{")+ 1: word.find("}")+1]  
                        entireFile[entireFile.index(word): entireFile.index(word)+1] = temp
                if("\\subsection*{" in word and "." in word):
                        subsections.append(index)
                        headings.append(word)
                        name = word[word.find(" ")+1:word.find("}")]
                        mathPeople.append(name)
                        name = ""
        #1/29/16 get all of the new commands
        comms = ''.join(entireFile[newCommands[0]:newCommands[1]])
        paras = []
        for i in range(len(subsections)-1):
                str = ''.join(entireFile[subsections[i]: subsections[i+1]-1])
                paras.append(str)
        sec = ""
        for f in headings:
                 for i in f:
                         try:
                                 int(i)
                                 sec += i
                         except:
                                 pass
                         if("." in i):
                                 sec+=i
                 sections.append(sec)
                 
                 sec = ""
        #sections now holds all sections

        numFile = ""
        filenums =  []
        for s in sections:
                numFile = ""
                if("." in s[0:2]):
                        numFile = s[0]
                else:
                        numFile = s[0:2]
                filenums.append(int(numFile))
        #filenums now has the file numbers like 1,9,14,etc
        
        #SO python is nothing like java, I have to read in the entire chapter
        #file and then change it and THEN put it back into the chapter file
        
        #chapter 9
        with open("tempchap9.tex", "r") as ch9:
                entire9 = ch9.readlines()
        ch9.close()
        #chapter 14
        with open("tempchap14.tex", "r") as ch14:
                entire14 = ch14.readlines()
        ch14.close()

        references9 = []
        footmiscIndex = 0
        index = 0
        beginIndex9= -1
        #now I have a list of the names, only store indices
        #of the paragraph if its in a section with these names
        #TODO make a method to do this
        canAdd = False
        for word in entire9:
                index+=1
                if("begin{document}" in word):
                        beginIndex9 += index
                if("footmisc" in word):
                        footmiscIndex+= index
                #need to check subsection and section because
                #KLSadd also fixes some subsections
                if("section{" in word or "subsection*{" in word):
                        w = word[word.find("{")+1:word.find("}")]
                        if(w in mathPeople):
                                canAdd = True
                if("\\subsection*{References}" in word and canAdd == True):
                        references9.append(index)
                        canAdd = False
        canAdd = False
        references14 = []
        index = 0
        footmiscIndex14 = 0
        beginIndex14 = -1
        for word in entire14:
                index+=1
                if("begin{document}" in word):
                        beginIndex14 += index
                if("footmisc" in word):
                        footmiscIndex14+= index
                #need to check subsection and section because
                #KLSadd also fixes some subsections
                if("section{" in word or "subsection*{" in word):
                        w = word[word.find("{")+1:word.find("}")]
                        if(w in mathPeople):
                                canAdd = True
                if("\\subsection*{References}" in word and canAdd == True):
                        references14.append(index)
                        canAdd = False
        #references9 is now full of indexes to put fixed paragraphs

        #TODO make into a method
        with open("newtempchap09.tex", "w") as temp9:
                count = 0

                #1/29/16 add hyperref, xparse, cite packages after the footmisc package
                entire9[footmiscIndex] += "\\usepackage[pdftex]{hyperref} \n\\usepackage {xparse} \n\\usepackage{cite} \n"
                #1/29/16 add in the newcommands from KLSadd.tex
                entire9[beginIndex9-1] += comms 
                #1/27/16 add \large\bf KLSadd: after every paragraph{
                for i in references9:
                        entire9[i-3] += "% RS: add begin"
                        entire9[i-3] += paras[count]
                        entire9[i-3] += "% RS: add end"
                        count+=1
                entire9[i-1] += paras[count] 

                
                str = ''.join(entire9)
                temp9.write(str)
        


       #works, as far as I know, huzzah
       #references14 is now full of indexes to put fixed paragraphs
        with open("newtempchap14.tex", "w") as temp14:
                entire14[footmiscIndex14] += "\\usepackage[pdftex]{hyperref} \n\\usepackage {xparse} \n\\usepackage{cite} \n"
                entire14[beginIndex14 -3] += comms 
                for i in references14:
                        entire14[i-3] += " RS: add begin"
                        entire14[i-3] += paras[count]
                        #entire14[i-3] += "% RS: add end"
                        count+=1
                str = ''.join(entire14)
                temp14.write(str)
        

        


