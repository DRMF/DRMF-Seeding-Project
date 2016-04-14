"""
Rahul Shah
self-taught python don't kill me I know its bad
2/5/16
Re-write of linetest.py so people other than me can read it
This project was/is being written to streamline the update process of the book used
for the online repository, updated via the KLSadd addendum file which only affects chapters
9 and 14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NOTE! AS OF 2/26/16 THIS FILE IS NOT YET UPDATED TO THE FULL CAPACITY OF THE PREVIOUS FILE. IF FURTHER DEVELOPMENT IS NEEDED, REFER TO THE
linetest.py FILE IF THIS FILE DOES NOT ADDRESS THE NEW/EXTRA GOALS. This means that XCITE PARSE etc HAS NOT BEEN ADDED
Additional goals (already addressed in linetest.py):
-insert correct usepackages
-insert correct commands found in KLSadd.tex to chapter files
-insert editor's initials into sections (ie %RS: begin addition, %RS: end addition)
Additional goals (not already addressed in linetest.py):
-rewrite for "smarter" edits (ex. add new limit relations straight to the limit relations section in the section itself, not at the end)
Current update status: incomplete
Goals:change the book chapter files to include paragraphs from the addendum, and after that insert some edits so they are intelligently integrated into the chapter
"""

#start out by reading KLSadd.tex to get all of the paragraphs that must be added to the chapter files
#also keep track of which chapter each one is in

#variables: chapNums for the chapter number each section belongs to paras will hold the sections that will be copied over
#chapNums is needed to know which file to open (9 or 14)
#mathPeople is just the name for the sections that are used, like Wilson, Racah, etc. I know some are not people, its just a var name
#yes I like lists
chapNums = []
paras = []
mathPeople = []
newCommands = [] #used to hold the indexes of the commands
comms = "" #holds the ACTUAL STRINGS of the commands
#2/18/16 this method addresses the goal of hardcoding in the necessary packages to let the chapter files run as pdf's.
#Currently only works with chapter 9, ask Dr. Cohl to help port your chapter 14 output file into a pdf

def prepareForPDF(chap):
    footmiscIndex = 0
    index = 0
    for word in chap:
        index+=1
        if("footmisc" in word):
            footmiscIndex+= index
    #edits the chapter string sent to include hyperref, xparse, and cite packages
    #str[footmiscIndex] += "\\usepackage[pdftex]{hyperref} \n\\usepackage {xparse} \n\\usepackage{cite} \n"
    chap.insert(footmiscIndex, "\\usepackage[pdftex]{hyperref} \n\\usepackage {xparse} \n\\usepackage{cite} \n")

    return chap

#2/18/16 this method reads in relevant commands that are in KLSadd.tex and returns them as a list and also adds

def getCommands(kls):
    index = 0
    for word in kls:
        index+=1
        if("smallskipamount" in word):
            newCommands.append(index-1)
        if("mybibitem[1]" in word):
            newCommands.append(index)
           #add \large\bf KLSadd: to make KLSadd additions appear like the other paragraphs
    #pretty sure I had to do something here but I forgot, so pass?
    #duh, obviously I need to store the commands somewhere!
    comms = kls[newCommands[0]:newCommands[1]]
    return comms

#2/18/16 this method addresses the goal of hardcoding in the necessary commands to let the chapter files run as pdf's. Currently only works with chapter 9

def insertCommands(kls, chap, cms):
    #reads in the newCommands[] and puts them in chap
    beginIndex = -1 #the index of the "begin document" keyphrase, this is where the new commands need to be inserted.

    #find index of begin document in KLSadd
    index = 0
    for word in kls:
        index+=1
        if("begin{document}" in word):
            beginIndex += index
    tempIndex = 0
    for i in cms:
        chap.insert(beginIndex+tempIndex,i)
        tempIndex +=1
    return chap

#method to find the indices of the reference paragraphs
def findReferences(chapter):
    references = []
    index = -1
    chaptercheck = 0
    if chapticker == 0:
        chaptercheck = str(9)
    elif chapticker == 1:
        chaptercheck = str(14)
    canAdd = False
    for word in chapter:
        index+=1
        #check sections and subsections
        if("section{" in word or "subsection*{" in word) and ("subsubsection*{" not in word):
            w = word[word.find("{")+1: word.find("}")]
            ws = word[word.find("{")+1: word.find("~")]
            for unit in mathPeople:
                subunit = unit[unit.find(" ")+1: unit.find("#")]
                if ((w in subunit) or (ws in subunit)) and (chaptercheck in unit) and (len(w) == len(subunit)) or (("Pseudo Jacobi" in w) and ("Pseudo Jacobi (or Routh-Romanovski)" in subunit)):
                    canAdd = True
        if("\\subsection*{References}" in word) and (canAdd == True):
            references.append(index)
            canAdd = False

    return references

#method to change file string(actually a list right now), returns string to be written to file
#If you write a method that changes something, it is preffered that you call the method in here
def fixChapter(chap, references, p, kls):
    #chap is the file string(actually a list), references is the specific references for the file,
    #and p is the paras variable(not sure if needed) kls is the KLSadd.tex as a list
    count = 0 #count is used to represent the values in count
    designator = 0 #Tells which chapter it's on
    if chapticker2 == 0:
        designator = "9."
    elif chapticker2 == 1:
        designator = "14."
    designator = str(designator)
    for i in references:
        #Place before References paragraph
        if count > 34:
            word1 = "14. Banana"
        else:
            word1 = str(p[count])
        if (designator in word1[word1.find("\\subsection*{") + 1: word1.find("}") ]):
            chap[i-2] += "%Begin KLSadd additions"
            chap[i-2] += p[count]
            chap[i-2] += "%End of KLSadd additions"
            count += 1
        else:
            while (designator not in word1[word1.find("\\subsection*{") + 1: word1.find("}") ]):
                word1 = str(p[count])
                if (designator in word1[word1.find("\\subsection*{") + 1: word1.find("}") ]):
                    chap[i - 2] += "%Begin KLSadd additions"
                    chap[i - 2] += p[count]
                    chap[i - 2] += "%End of KLSadd additions"
                    count += 1
                else:

                    count+=1
    chap = prepareForPDF(chap)
    cms = getCommands(kls)
    chap = insertCommands(kls,chap, cms)
    commentticker = 0
    for word in chap:
        word2 = chap[chap.index(word)-1]
        if ("\\newcommand{\qhypK}[5]{\,\mbox{}_{#1}\phi_{#2}\!\left(" not in word2):
            if ("\\newcommand\\half{\\frac12}" in word):
                wordtoadd = "%" + word
                chap[commentticker] = wordtoadd
            elif ("\\newcommand{\\hyp}[5]{\\,\\mbox{}_{#1}F_{#2}\\!\\left(" in word):
                wordtoadd = "%" + word
                chap[commentticker] = wordtoadd
            elif ("\\genfrac{}{}{0pt}{}{#3}{#4};#5\\right)}" in word):
                wordtoadd = "%" + word
                chap[commentticker] = wordtoadd
            elif ("\\newcommand{\\qhyp}[5]{\\,\\mbox{}_{#1}\\phi_{#2}\\!\\left(" in word):
                wordtoadd = "%" + word
                chap[commentticker] = wordtoadd
        commentticker += 1
        # Hopefully this works
    ticker1 = 0
    while ticker1 < len(chap):
        if ('\\myciteKLS' in chap[ticker1]):
            chap[ticker1] = chap[ticker1].replace('\\myciteKLS', '\\cite')
        ticker1 += 1
    #probably won't work because I don't know how anything works
    return chap

#open the KLSadd file to do things with
with open("KLSadd.tex", "r") as add:
    #store the file as a string
    addendum = add.readlines()
    for word in addendum:
        if ("paragraph{" in word):
            lenword = len(word) - 1
            temp = word[0:word.find("{") + 1] + "\large\\bf KLSadd: " + word[word.find("{") + 1: lenword]
            addendum[addendum.index(word)] = temp
        if ("subsubsection*{" in word):
            lenword = len(word) - 1
            addendum[addendum.index(word)] = word[0:word.find("{") + 1] + "\large\\bf KLSadd: " + word[word.find("{") + 1: lenword]
    index = 0
    indexes = []
    for word in addendum:
        index+=1
        if("." in word and "\\subsection*{" in word):
            if ("9." in word):
                chapNums.append(9)
                name = word[word.find("{") + 1: word.find("}") ]
                mathPeople.append(name + "#")
            if("14." in word):
                chapNums.append(14)
                name = word[word.find("{") + 1: word.find("}") ]
                mathPeople.append(name + "#")
            #get the index
            indexes.append(index-1)
    #now indexes holds all of the places there is a section
    #using these indexes, get all of the words in between and add that to the paras[]
    for i in range(len(indexes)-1):
        box = ''.join(addendum[indexes[i]: indexes[i+1]-1])
        paras.append(box)
    paras.append("% This is a test")
    #paras now holds the paragraphs that need to go into the chapter files, but they need to go in the appropriate
    #section(like Wilson, Racah, Hahn, etc.) so we use the mathPeople variable
    #we can use the section names to place the relevant paragraphs in the right place

    #as of 2/8/16 the paragraphs will go before the References paragraph of the relevant section
    #parse both files 9 and 14 as strings

    #chapter 9
    with open("chap09.tex", "r") as ch9:
        entire9 = ch9.readlines() #reads in as a list of strings
    ch9.close()

    #chapter 14
    with open("chap14.tex", "r") as ch14:
        entire14 = ch14.readlines()
    ch14.close()
    #call the findReferences method to find the index of the References paragraph in the two file strings
    #two variables for the references lists one for chapter 9 one for chapter 14
    chapticker = 0
    references9 = findReferences(entire9)
    chapticker += 1
    references14 = findReferences(entire14)
    #call the fixChapter method to get a list with the addendum paragraphs added in
    chapticker2 = 0
    str9 = ''.join(fixChapter(entire9, references9, paras, addendum))
    chapticker2 += 1
    str14 = ''.join(fixChapter(entire14, references14, paras, addendum))

"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you are writing something that will make a change to the chapter files, write it BEFORE this line, this part
is where the lists representing the words/strings in the chapter are joined together and updated as a string!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


#write to files
#new output files for safety
with open("updated9.tex","w") as temp9:
    temp9.write(str9)

with open("updated14.tex", "w") as temp14:
    temp14.write(str14)