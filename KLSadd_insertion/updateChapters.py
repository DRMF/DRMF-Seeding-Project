"""
Rahul Shah
self-taught python don't kill me I know its bad 
2/5/16 
Re-write of linetest.py so people other than me can read it

This project was/is being written to streamline the update process of the book used
for the online repository, updated via the KLSadd addendum file which only affects chapters
9 and 14

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NOTE! AS OF 2/8/16 THIS FILE IS NOT YET UPDATED TO THE FULL CAPACITY OF THE PREVIOUS FILE. IF FURTHER DEVELOPMENT IS NEEDED, REFER TO THE
linetest.py FILE IF THIS FILE DOES NOT ADDRESS THE NEW/EXTRA GOALS. This means that XCITE PARSE etc HAS NOT BEEN ADDED

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
def fixChapter(str, references, p):
        #str is the file string, references is the specific references for the file, and p is the paras variable(not sure if needed)
        #TODO: OPTIMIZE
        count = 0 #count is used to represent the values in count
        for i in references:
                #add
                str[i-3] += p[count] 
                count+=1
        #I actually don't remember why I had to do this but I think you need it
        str[i-1] += p[count]
        return str

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
        
        #call the fixChapter method to get a list with the addendum paragraphs added in
        str9 = ''.join(fixChapter(entire9, references9, paras))
        str14 = ''.join(fixChapter(entire14, references14, paras))

        #write to file
        #new output files for safety
        with open("updated9.tex","w") as temp9:
                temp9.write(str9)
        temp9.close()

        with open("updated14.tex", "w") as temp14:
                temp14.write(str9)
        
