"""
Rahul Shah
11/20/15
FileChangerLatex.py
Reads in from KLSadd.tex, finds places to be changed and adds
to end of section
"""

#Open the document to be read
#Figure out which chapter to read

subsection = ""
a = -1
chapter ="" 
list = []
with open("KLSadd.tex", "rb") as file:
        for line in file:
                #finds all mentions of subsections in KLSadd
                #used to determine chapter number
                #tests every subsection to find if it has a number
                #eliminates Introduction, etc
                chapter = ""
                subsection = ""
                toCopy = False
                if("\\subsection*{" in line):
                        #finds the subsection and subsubsections
                        for word in line:
                                try:
                                        chapter+= str(int(word))
                                except: 
                                        a = -1 
                         
                                if(word =="."):
                                        chapter += "." 

                        if(chapter is not ""):
                                list.append(chapter)
        #END OF LOOP why can't I have nice brackets like java :(
        """
        list contains all of the subsections. Begin chapter file searching
        """
        words = ""
        for line2 in file:
                words += line2

        print(words)
        numFile = ""
        fileList = []
        for s in list:
                numFile = ""
                if("." in s[0:2]):
                        numFile = s[0]
                else:
                        numFile = s[0:2]
                fileList.append(int(numFile))

        #numFile now contains the right number of the file to access
        #stored in fileList
               

         

                file.close()
#end of FileChangerLatex.py
