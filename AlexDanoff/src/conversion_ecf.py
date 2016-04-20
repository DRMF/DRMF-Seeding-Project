#Divya Gandla
#Master Code

import re

#existing file named text.txt
file=open('test1.txt','r').read()
    
#output written to newText.txt
newFile=open('newIdentities.txt','w')

listOfGVars=["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma",
    "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega", "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "Xi", "Omicron", "Pi", "Rho", "Sigma",
    "tau", "upsilon", "phi", "chi", "psi", "omega"]

def replaceGreekVars(s):
    newFile=s;
    for gvar in listOfGVars:
        #original ex: \[Delta]
        oldGVar="\[" + gvar + "]";
        
        #replacement ex: \delta
        newGVar= chr(92) + gvar.lower();
        newFile=(newFile.replace(oldGVar, newGVar));
        
        #adds a space after the replacement of the greek letter if it's followed by A-Z or a-z
        for i in range(len(newFile)):
            if newFile[i:i+len(newGVar)]== newGVar:
                if ord(newFile[i+len(newGVar): i+len(newGVar)+1]) >= 65 and ord(newFile[i+len(newGVar): i+len(newGVar)+1]) <= 90:
                    newFile=(newFile.replace(newGVar, newGVar+" "));
                elif ord(newFile[i+len(newGVar): i+len(newGVar)+1]) >= 97 and ord(newFile[i+len(newGVar): i+len(newGVar)+1]) <= 122:
                    newFile=newFile.replace(newGVar, newGVar+" ");
                        
        #special case: replace "pi" with "\cpi" <-- circular pi
        newFile=newFile.replace("Pi","\cpi");
        
  
    return newFile;
     
def findArgs(s, functionName):
    newReplacings=[]

    #finds capture groups (includes brackets in arguments)
    replacings=(re.findall(r''+ functionName + '(\[.*\])',s))
    for i in replacings:
        recurse=i.find(functionName)
        #if the function name is found in the replacing, regex is used to find the inner function's arguments
        #regex's string is from the position of the function name till the end
        replacings.extend(re.findall(r''+ functionName + '(\[.*\])',i[recurse:]))
        if recurse>=0:
            #if the function name is found in the replacing, regex is used to find the inner function's arguments
            #regex's string is from the position of the last instance(of function name) plus the length(of function name) till the end
            replacings.extend(re.findall(r''+ functionName + '(\[.*\])',i[recurse+len(functionName):]))

    #gets rid of extra ]
    for i in replacings:
        countOpen=0
        countClose=0
        position=0
        for char in i:
            if char=='[':
                countOpen=countOpen+1
            elif char==']':
                countClose=countClose+1
            #if the num open and close are same, the string is appended till that location
            if countOpen==countClose:
                newReplacings.append(i[0:position+1])
                break            
            position=position+1
                        
    return newReplacings

def replaceSqrt(s):
    arguments=findArgs(s, "Sqrt")
    for i in arguments:
        s=s.replace("Sqrt"+ i, "\\sqrt{" + i[1:len(i)-1] + "}")
    return(s)

def replacePolygamma(s):
    arguments=findArgs(s, "Polygamma")
    for i in arguments:
        commaLoc=i.find(',')
        if i[1:2] != "0":
            s=s.replace("Polygamma" +i, "\\polygamma{" + i[1:commaLoc]+"}@{" +i[commaLoc+1:len(i)-1]+ "}")
        elif i[1:2] == "0":
            s=s.replace("Polygamma" +i, "\\digamma@{" + i[3:len(i)-1] +"}")
    return s

def removeInactive(s):
    arguments=findArgs(s, "Inactive")
    for i in arguments:
        s=s.replace("Inactive"+i, i[1:len(i)-1])
    return s

def replaceCos(s):
    arguments=findArgs(s, "Cos")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Cos"+i,"\\cos@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Cos"+i,"\\cos@{"+i[1:len(i)-1]+"}")
    return s

def replaceSin(s):
    arguments=findArgs(s, "Sin")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Sin"+i,"\\sin@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Sin"+i,"\\sin@{"+i[1:len(i)-1]+"}")
    return s

def replaceTan(s):
    arguments=findArgs(s, "Tan")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Tan"+i,"\\tan@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Tan"+i,"\\tan@{"+i[1:len(i)-1]+"}")
    return s

def replaceCsc(s):
    arguments=findArgs(s, "Csc")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Csc"+i,"\\csc@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Csc"+i,"\\csc@{"+i[1:len(i)-1]+"}")
    return s

def replaceSec(s):
    arguments=findArgs(s, "Sec")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Sec"+i,"\\sec@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Sec"+i,"\\sec@{"+i[1:len(i)-1]+"}")
    return s

def replaceCot(s):
    arguments=findArgs(s, "Cot")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Cot"+i,"\\cot@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Cot"+i,"\\cot@{"+i[1:len(i)-1]+"}")
    return s
def replaceCosh(s):
    arguments=findArgs(s, "Cosh")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Cosh"+i,"\\cosh@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Cosh"+i,"\\cosh@{"+i[1:len(i)-1]+"}")
    return s

def replaceSinh(s):
    arguments=findArgs(s, "Sinh")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Sinh"+i,"\\sinh@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Sinh"+i,"\\sinh@{"+i[1:len(i)-1]+"}")
    return s

def replaceTanh(s):
    arguments=findArgs(s, "Tanh")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Tanh"+i,"\\tanh@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Tanh"+i,"\\tanh@{"+i[1:len(i)-1]+"}")
    return s

def replaceCsch(s):
    arguments=findArgs(s, "Csch")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Csch"+i,"\\csch@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Csch"+i,"\\csch@{"+i[1:len(i)-1]+"}")
    return s

def replaceSech(s):
    arguments=findArgs(s, "Sech")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Sech"+i,"\\sech@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Sech"+i,"\\sech@{"+i[1:len(i)-1]+"}")
    return s

def replaceCoth(s):
    arguments=findArgs(s, "Coth")
    for i in arguments:
        if len(i)==3:
            s=s.replace("Coth"+i,"\\coth@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("Coth"+i,"\\coth@{"+i[1:len(i)-1]+"}")
    return s
            
def replaceArcCos(s):
    arguments=findArgs(s, "ArcCos")
    for i in arguments:
        if len(i)==3:
            s=s.replace("ArcCos"+i,"\\acos@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("ArcCos"+i,"\\acos@{"+i[1:len(i)-1]+"}")
    return s

def replaceArcSin(s):
    arguments=findArgs(s, "ArcSin")
    for i in arguments:
        if len(i)==3:
            s=s.replace("ArcSin"+i,"\\asin@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("ArcSin"+i,"\\asin@{"+i[1:len(i)-1]+"}")
    return s

def replaceArcTan(s):
    arguments=findArgs(s, "ArcTan")
    for i in arguments:
        if len(i)==3:
            s=s.replace("ArcTan"+i,"\\atan@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("ArcTan"+i,"\\atan@{"+i[1:len(i)-1]+"}")
    return s

def replaceArcCsc(s):
    arguments=findArgs(s, "ArcCsc")
    for i in arguments:
        if len(i)==3:
            s=s.replace("ArcCsc"+i,"\\acsc@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("ArcCsc"+i,"\\acsc@{"+i[1:len(i)-1]+"}")
    return s

def replaceArcSec(s):
    arguments=findArgs(s, "ArcSec")
    for i in arguments:
        if len(i)==3:
            s=s.replace("ArcSec"+i,"\\asec@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("ArcSec"+i,"\\asec@{"+i[1:len(i)-1]+"}")
    return s

def replaceArcCot(s):
    arguments=findArgs(s, "ArcCot")
    for i in arguments:
        if len(i)==3:
            s=s.replace("ArcCot"+i,"\\acot@@{"+i[1:len(i)-1]+"}")
        else:
            s=s.replace("ArcCot"+i,"\\acot@{"+i[1:len(i)-1]+"}")
    return s

def replaceInfinity(s):
    recurse=s.find("Infinity")
    while recurse>=0:
        s=s.replace("Infinity", "\infty")
        recurse=s.find("Infinity")
    return s

def ContinuedFractionK(s):
    arguments=findArgs(s, "ContinuedFractionK")
    for i in arguments:
        location=i.find(",{")
        if location<0:
            location=i.find(", {")
        var=i[1:location]
        s=s.replace("ContinuedFractionK"+i, "\ContinuedFractionK{k}{1}{\infty}@{"+var+"}")
    return s
            
def replaceAbs(s):
    arguments=findArgs(s, "Abs")
    for i in arguments:
        s=s.replace("Abs"+i, "\Abs@{"+i[1:len(i)-1]+"}")
    return s

def comparativeRelators(s):
    s=s.replace("LessEqual", "\\leq")
    s=s.replace("Less", "<")
    return s

def element(s):
    #http://texblog.org/2007/08/27/number-sets-prime-natural-integer-rational-real-and-complex-in-latex/
    arguments=findArgs(s,"Element")
    for i in arguments:
        location=i.rfind(", ")
        if location<0:
            location=i.rfind(",")

        if location>=0:
            var=i[location+1:len(i)-1].strip()
            z=i[1:location].strip()

            if (var=="Complexes"):
                s=s.replace("Element"+i, z+" \in \Complex")
            elif (var=="Wholes"):
                s=s.replace("Element"+i, z+" \in \Whole")
            elif (var=="Naturals"):
                s=s.replace("Element"+i, z+" \in \\NatNumber")
            elif (var=="Integers"):
                s=s.replace("Element"+i, z+" \in \Integer")
            elif (var=="Irrationals"):
                s=s.replace("Element"+i, z+" \in \Irrational")
            elif (var=="Reals"):
                s=s.replace("Element"+i, z+" \in \Real")
            elif (var=="Rational"):
                s=s.replace("Element"+i, z+" \in \Rational")
            elif (var=="Primes"):
                s=s.replace("Element"+i, z+" \in \Prime")
        return s

def markup(file):

    newFile=""
    equations=findArgs(file,"ConditionalExpression")
    constraints=[]
    
    #looks through each equation set including the conditional expression
    for index in range(len(equations)):
        equation=equations[index]
        location=equation.find(", Element")
        if location==-1:
            location=equation.find(",Element")
	#there are no constraints if Element[ ] is not found
        if location==-1:
            location=len(equation)

        newFile=newFile+"\\begin{equation} \n" + equation[1:location] + "%  \\constraints{\n"

	#find constraints
        c=findArgs(equation,"Element")
        for element in c:
            location=element.rfind(", ")
            if location<0:
                location=element.rfind(",")
            if location>=0:
                var=element[location+1:len(element)-1].strip()
                z=element[1:location].strip()
            elif element.count("|") >0:
                for index in range(element.count("|")+1):
                    #if it is the first constraints then it is from beginning to the first location of the |, the loc is increased each time to get through all of the constraints
                    if index==0:
                        loc=element.find("|")
                        constraints.append(element[1:loc])
                    elif index==element.count:
                        loc=element.find("|", loc+1)
                        constraints.append(element[loc, element.find(",")])
                    else:
                        constraints.append(element[loc:element.find("|", loc+1)])
                        loc=element.find("|", loc+1)
        print(var)	
	    
        for index in range(len(constraints)):
            print(constraints)
            if (var=="Complexes"):
                newFile="%      "+ newFile+ constraints+ "\in \Complex"
            elif (var=="Wholes"):
                newFile="%      "+ newFile+ constraints+ "\in \\NonNegInteger"
            elif (var=="Naturals"):
                newFile="%      "+ newFile+ constraints+ "\in \\NatNumber"
            elif (var=="Integers"):
                newFile="%      "+ newFile+ constraints+ "\in \Integer"
            elif (var=="Irrationals"):
                newFile="%      "+ newFile+ constraints+ "\in \Irrationals"
            elif (var=="Reals"):
                newFile="%      "+ newFile+ constraints+ "\in \Real"
            elif (var=="Rational"):
                newFile="%      "+ newFile+ constraints+ "\in \Rational"
            elif (var=="Primes"):
                newFile="%      "+ newFile+ constraints+ "\in \Prime"
    return newFile

def equationSetUp(s):


    newFile="\\begin {equation}\n"
    start=s.find("ConditionalExpression[")+ len("ConditionalExpression[")
    end=s.rfind(",")
    end=s.rfind(",",0,end)
    newFile=newFile+s[start:end]+"\n" 
    constraints=[]
    if (s.find("Element["))>0:
        elements=s[s.find("Element[",end)+ len("Element["): len(s)-1]
        newFile=newFile+"%  \constraints{\n"
        numCon=elements.count("|")+1
        location=0
        for index in range(numCon):
            if index==0:
                if numCon==1:
                    constraints.append(elements[0:elements.find(",")].strip())
                else:
                    location=elements.find("|")
                    constraints.append(elements[0:location].strip())
            elif index==numCon-1:
                constraints.append(elements[location+1:elements.find(",",location)].strip())
            else:
                constraints.append(elements[location+1:elements.find("|", location+1)].strip())
                location=elements.find("|", location+1)
        var=elements[elements.rfind(",")+1:len(elements)-1].strip()
        for index in range(len(constraints)):
            if index==len(constraints)-1:
                if (var=="Complexes"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Complex }\n"
                elif (var=="Wholes"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \\NonNegInteger }\n"
                elif (var=="Naturals"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \\NatNumber }\n"
                elif (var=="Integers"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Integer }\n"
                elif (var=="Irrationals"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Irrationals }\n"
                elif (var=="Reals"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Real }\n"
                elif (var=="Rational"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Rational }\n"
                elif (var=="Primes"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Prime }\n"
            else:
                if (var=="Complexes"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Complex &\n"
                elif (var=="Wholes"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \\NonNegInteger &\n"
                elif (var=="Naturals"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \\NatNumber &\n"
                elif (var=="Integers"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Integer &\n"
                elif (var=="Irrationals"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Irrationals &\n"
                elif (var=="Reals"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Real &\n"
                elif (var=="Rational"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Rational &\n"
                elif (var=="Primes"):
                    newFile=newFile+"%      "+ constraints[index]+ " \in \Prime &\n"
    return(newFile+"\\end {equation} \n\n")


file=removeInactive(file)
file=replaceGreekVars(file)
file=replaceSqrt(file)
file=replacePolygamma(file)
file=replaceCos(file)
file=replaceSin(file)
file=replaceTan(file)
file=replaceCsc(file)
file=replaceSec(file)
file=replaceCot(file)
file=replaceArcCos(file)
file=replaceArcSin(file)
file=replaceArcTan(file)
file=replaceArcCsc(file)
file=replaceArcSec(file)
file=replaceArcCot(file)
file=replaceCosh(file)
file=replaceSinh(file)
file=replaceTanh(file)
file=replaceCsch(file)
file=replaceSech(file)
file=replaceCoth(file)
file=replaceInfinity(file)
file=ContinuedFractionK(file)
file=replaceAbs(file)
file=comparativeRelators(file)


count=0
position=0
yorn=False
for index in range(len(file)):
    if file[index: index+2]=="(*":
        count=index
        position=file.find("\n", index)
        position=file.find("\n", position+1)
        newFile.write(equationSetUp(file[index: position]).replace("*"," "))
newFile.close()
