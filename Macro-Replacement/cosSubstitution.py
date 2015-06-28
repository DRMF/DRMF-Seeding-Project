import sys
input=sys.argv[1]
text=open(input,"r") #READ FILE
lines=text.readlines()
text.close()
toWrite=""
p=""
math=False
substitution=False
def checkEq(equation):
	   theta=False
	   phi=False
	   x=False
	   if "\\theta" in equation:
			 theta=True
	   if "\\phi" in equation:
			 phi=True
	   mac=False
	   for c in equation:
			 if c=="\\":
				    mac=True
			 if not c.isalpha():
				    mac=False
			 if not mac and c=="x":
				    x=True
				    break
	   if x and theta and not phi:
			 return("$x=\\cos@@{\\theta}$ ")
	   elif x and theta and phi:
			 return("$x=\\cos@{\\theta+\\phi}$ ")
	   else:
			 return("")

for line in lines:
	   if "\\begin{equation}" in line:
			 math=True
			 equation=""
			 subLine=""
	   if "\\end{equation}" in line:
			 math=False
			 substitution=False
			 p=checkEq(equation)
			 if p!="" and not ("$x=\\cos@@{\\theta}$" in subLine or "$x=\\cos@{\\theta+\\phi}$" in subLine):
				    #print equation+"\n"+subLine
				    if subLine=="":
						  toWrite+="%  \substitution{"+p+"}\n"
				    else:
						  subLine=subLine.strip("\n")
						  subLine=subLine.strip("}")+"\n"
						  toWrite+=subLine+"%     "+p+"}\n"
			 else:toWrite+=subLine
	   if "\\substitution" in line:
			 substitution=True
			 math=False
			 subLine=""
	   if math:
			 equation+=line.replace("\n"," ")
			 toWrite+=line
	   elif substitution:
			 subLine+=line
	   else:
			 toWrite+=line
text=open(sys.argv[2],"w") #OUTPUT FILE
text.write(toWrite)
