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
               if("paragraph{" in word):
                        #not sure if this works, needs testing!
                        temp = word[0:word.find("{")+ 1] + "\large\\bf KLSadd: " + word[word.find("{")+ 1: word.find("}")+1]

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
        for w in kls:
                index+=1
                if("begin{document}" in word):
                        beginIndex += index
        tempIndex = 0
        #D'OH FOUND THE PROBLEM newCommands stores just the integer value of the indexes of the commands. we need to get the actual commands. easy fix, do next time
        for i in cms:
                chap.insert(beginIndex+tempIndex,i)
                tempIndex +=1
        return chap

#method to find the indices of the reference paragraphs
def findReferences(str):
        references = []
        index = -1
        canAdd = False
        for word in str:
                index+=1
                #check sections and subsections
                if("section{" in word or "subsection*{" in word):
                        w = word[word.find("{")+1: word.find("}")]
                        if(w not in mathPeople):
                                canAdd = True
                if("\\subsection*{References}" in word and canAdd == True):
                        references.append(index)
                        canAdd = False
        return references

#method to change file string(actually a list right now), returns string to be written to file
#If you write a method that changes something, it is preffered that you call the method in here
def fixChapter(chap, references, p, kls):
        #chap is the file string(actually a list), references is the specific references for the file,
        #and p is the paras variable(not sure if needed) kls is the KLSadd.tex as a list
        #TODO: OPTIMIZE(?)
        count = 0 #count is used to represent the values in count
        for i in references:
                #add the paragraphs before the Reference paragraphs start
                chap[i-3] += p[count] 
                count+=1
        chap[i-1] += p[count]

        #I actually don't remember why I had to do this but I think you need it ^^^^^^^^^^^^^^^^^^^ 
        chap = prepareForPDF(chap)
        cms = getCommands(kls)
        chap = insertCommands(kls,chap, cms)
        #probably won't work because I don't know how anything works
        return chap

#open the KLSadd file to do things with 
with open("KLSadd.tex", "r") as add:
        #store the file as a string
        addendum = add.readlines()
        index = 0
        indexes = []
        for word in addendum:
                index+=1
                if("." in word and "\\subsection*{" in word):
                        name = word[word.find(" "): word.find("}")]
                        mathPeople.append(name)
                        if("9." in word):
                                chapNums.append(9)
                        if("14." in word):
                                chapNums.append(9)
                        #get the index
                        indexes.append(index-1)
        #now indexes holds all of the places there is a section
        #using these indexes, get all of the words in between and add that to the paras[]
        for i in range(len(indexes)-1):
                str = ''.join(addendum[indexes[i]: indexes[i+1]-1])
                paras.append(str)

        #paras now holds the paragraphs that need to go into the chapter files, but they need to go in the appropriate
        #section(like Wilson, Racah, Hahn, etc.) so we use the mathPeople variable
        #we can use the section names to place the relevant paragraphs in the right place
        
        #as of 2/8/16 the paragraphs will go before the References paragraph of the relevant section
        #parse both files 9 and 14 as strings

        #chapter 9
        with open("tempchap9.tex", "r") as ch9:
                entire9 = ch9.readlines() #reads in as a list of strings
        ch9.close()
        
        #chapter 14
        with open("tempchap14.tex", "r") as ch14:
                entire14 = ch14.readlines()
        ch14.close()
        #call the findReferences method to find the index of the References paragraph in the two file strings 
        #two variables for the references lists one for chapter 9 one for chapter 14
        references9 = findReferences(entire9)
        references14 = findReferences(entire14)

        #ERROR! entire9 sometimes contains lists, must only contain strings. Should be fixed by next week. Check the 
        #getCommands method, I suspect that is the problem
        #call the fixChapter method to get a list with the addendum paragraphs added in
        str9 = ''.join(fixChapter(entire9, references9, paras, addendum))
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
        temp14.write(str9)
