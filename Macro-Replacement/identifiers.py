import sys, re

def searchAll(match):
    """Determines which macros are present in a given match and creates the corresponding identifier string."""
    tempstring = ":"
    global all_funcs

    for func in all_funcs:

        abbr = func.abbr
        num = func.count(match)

        #more than zero matches
        if num > 0:
            tempstring += "{abbr} {num}:".format(**locals())

    return tempstring

def _replace(match):

    pattern = re.compile(r'\\end{' + match.group(1) + '}')
    if (re.search(pattern, match.group(2)) != None or re.search(pattern, match.group(3)) != None):
        return match.group()

    tempstring = '\\begin{' + match.group(1) + '}\\label{' + match.group(3) + '}%'
    tempstring += searchAll(match.group(2))
    tempstring += match.group(2) + '\\end{' + match.group(1) + '}'
    return tempstring

def _replace2(match):
    pattern = re.compile(r'\\label{')
    if (re.search(pattern, match.group(2)) != None):
        return match.group()
    tempstring = '\\begin{' + match.group(1) + '}%'
    tempstring += searchAll(match.group(2))
    tempstring += match.group(2) + '\n\\end{' + match.group(1) + '}'
    return tempstring

def replace2(match):
    tempstring = '\\begin{' + match.group(1) + '}\\label{' + match.group(3) + '}%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    pattern3 = re.compile(r'\\end{')
    if (re.search(pattern, match.group(2)) != None or re.search(pattern2, match.group(2)) != None or re.search(pattern3, match.group(2)) != None):
        return match.group()
    tempstring += searchAll(match.group(2))
    tempstring += match.group(2)
    return tempstring

def replace3(match):
    tempstring = '\\\\\n\\label{' + match.group(2) + '}' + '%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    if (re.search(pattern, match.group(1)) != None):
        return match.group()
    tempstring += searchAll(match.group(1))
    tempstring += match.group(1)
    return tempstring

def replace3v2(match):
    tempstring = '\\\\\n\\label{' + match.group(2) + '}' + '%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    if (re.search(pattern, match.group(1)) != None or re.search(pattern2, match.group(1)) != None):
        return match.group()
    tempstring += searchAll(match.group(1))
    tempstring += match.group(1)
    return tempstring

def replace4(match):
    tempstring = '\\\\\n\\nonumber%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    if (re.search(pattern2, match.group(1)) != None):
        return match.group()
    tempstring += searchAll(match.group(1))
    tempstring += match.group(1)
    return tempstring

def replace5(match):
    tempstring = '\\begin{' + match.group(1) + '}\\nonumber%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    if (re.search(pattern, match.group(2)) != None or re.search(pattern2, match.group(2)) != None):
        return match.group()
    tempstring += searchAll(match.group(2))
    tempstring += match.group(2)
    return tempstring

def replace6(match):
    tempstring = '\\sLP\n\\nonumber%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    if (re.search(pattern2, match.group(1)) != None):
        return match.group()
    tempstring += searchAll(match.group(1))
    tempstring += match.group(1)
    return tempstring

def replace7(match):
    tempstring = '\\sLP\n\\label{' + match.group(2) + '}' + '%'
    pattern = re.compile(r'\\nonumber')
    pattern2 = re.compile(r'\\label{')
    if (re.search(pattern, match.group(1)) != None):
        return match.group()
    tempstring += searchAll(match.group(1))
    tempstring += match.group(1)
    return tempstring
    

def replacealign(match):

    matchstring = match.group()

    labelpattern1 = re.compile(r'\\begin{(align)}(.+?)\\label{(.*?)}', re.DOTALL)
    labelpattern2 = re.compile(r'\\\\(.+?)\\label{(.*?)}', re.DOTALL)

    labelpattern2v2 = re.compile(r'\\\\(?!\n\\nonumber)(.{2,}?)\\label{(.*?)}', re.DOTALL)

    labelpattern3 = re.compile(r'\\begin{(align)}(.+?)\\nonumber', re.DOTALL)
    labelpattern4 = re.compile(r'\\\\(.+?)\\nonumber', re.DOTALL)
    labelpattern5 = re.compile(r'\\sLP(.+?)\\nonumber', re.DOTALL)
    labelpattern6 = re.compile(r'\\sLP(.+?)\\label{(.*?)}', re.DOTALL)

    matchstring = re.sub(labelpattern1, replace2, matchstring)
    matchstring = re.sub(labelpattern3, replace5, matchstring)
    matchstring = re.sub(labelpattern2, replace3, matchstring)
    matchstring = re.sub(labelpattern4, replace4, matchstring)
    matchstring = re.sub(labelpattern5, replace6, matchstring)
    matchstring = re.sub(labelpattern6, replace7, matchstring)

    matchstring = re.sub(labelpattern2v2, replace3v2, matchstring)

    return matchstring

def eqnarray_rpl1(match):
    tempstring = '\\begin{' + match.group(1) + '}\\label{' + match.group(2) + '}%'
    tempstring += searchAll(match.group(3))
    if (re.match('\n', match.group(3)) == None):
        tempstring += '\n'
    tempstring += match.group(3) + match.group(4)
    return tempstring

def eqnarray_rpl2(match):
    tempstring = '\\\\\n\\nonumber%'
    tempstring += searchAll(match.group(1))
    if (re.match('\n', match.group(1)) == None):
        tempstring += '\n'
    tempstring += match.group(1) + match.group(2)
    return tempstring

def eqnarray_rpl3(match):
    tempstring = '\\\\\n\\nonumber%'
    tempstring += searchAll(match.group(1))
    if (re.match('\n', match.group(1)) == None):
        tempstring += '\n'
    tempstring += match.group(1)
    return tempstring

def eqnarray_replace(match):

    matchstring = match.group()

    pattern1 = re.compile(r'\\begin{(eqnarray)}\s*\\label{(.*?)}\s*(.*?)(\s*\\end{\1}|\\nonumber)', re.DOTALL)
    pattern2 = re.compile(r'\\nonumber\\\\\s+(.*?)(\s*\\end{eqnarray}|\\nonumber)', re.DOTALL)
    pattern3 = re.compile(r'(?<!\\nonumber)\\\\\s*(.+?)(?<!\n)\\nonumber', re.DOTALL)

    matchstring = re.sub(pattern1, eqnarray_rpl1, matchstring)
    matchstring = re.sub(pattern3, eqnarray_rpl3, matchstring)
    matchstring = re.sub(pattern2, eqnarray_rpl2, matchstring)
    matchstring = re.sub(pattern2, eqnarray_rpl2, matchstring)

    return matchstring


def replacestar(match):
    pattern = re.compile(r'\\label{')
    if (re.search(pattern, match.group(2)) != None):
        return match.group()
    tempstring = '\\begin{' + match.group(1) + '}%'
    tempstring += searchAll(match.group(2))
    if (re.match('\n', match.group(2)) == None):
        tempstring += '\n'
    tempstring += match.group(2) + '\n\\end{' + match.group(1) + '}'
    return tempstring

def equation_replace_kk(match):

    tempstring = '\\begin{' + match.group(1) + '}\\label{' + match.group(2) + r'}%'
    tempstring += searchAll(match.group(3))
    tempstring += '\n' + match.group(3) + '\\end{' + match.group(1) + '}'
    return tempstring

def LabelAll(content, functions):

    global all_funcs
    all_funcs = functions
    #searches and moves labels
    #{equation} -- Koekoek
    equationpattern = re.compile(r'\\begin{(equation)}\s+\\label{(.*?)}\s*(.*?)\\end{\1}', re.DOTALL)
    content = equationpattern.sub(equation_replace_kk, content)

    equationpattern = re.compile(r'\\begin{(equation)}(?!\\label)\s*(.*?)\s*\\end{\1}', re.DOTALL)
    content = equationpattern.sub(replacestar, content)

    #{equation} -- Koornwinder
    #equationpattern = re.compile(r'\\begin{(equation)}(.*?)\n\\end{equation}', re.DOTALL)
    #content = re.sub(equationpattern, _replace2, content)

    #FIX THIS
    #equationpattern = re.compile(r'\\begin{(equation)}(.*?)\\label{(.*?)}\n\\end{equation}', re.DOTALL)
    #content = re.sub(equationpattern, _replace, content)

    #{equation*}
    eqstarpattern = re.compile(r'\\begin{(equation\*)}(.*?)\n\\end{equation\*}', re.DOTALL)
    content = re.sub(eqstarpattern, replacestar, content)

    #{multline*}
    multstarpattern = re.compile(r'\\begin{(multline\*)}(.*?)\n\\end{multline\*}', re.DOTALL)
    content = re.sub(multstarpattern, replacestar, content)

    #{multline}
    multlinepattern = re.compile(r'\\begin{(multline)}(.*?)\\label{(.*?)}\n\\end{multline}', re.DOTALL)
    content = re.sub(multlinepattern, _replace, content)

    #{eqnarray}
    eqnarraypattern = re.compile(r'\\begin{(eqnarray)}(.*?)\\end{eqnarray}', re.DOTALL) 
    content = re.sub(eqnarraypattern, eqnarray_replace, content)

    #{eqnarray*}
    eqnstarpattern = re.compile(r'\\begin{(eqnarray\*)}\s*(.*?)\n\\end{eqnarray\*}', re.DOTALL)
    content = re.sub(eqnstarpattern, replacestar, content)
    
    #{align}
    alignpattern = re.compile(r'\\begin{(align)}(.*?)\\end{align}', re.DOTALL)
    content = re.sub(alignpattern, replacealign, content)
    checkalignpattern = re.compile(r'\n\n\\end{align}', re.DOTALL)
    content = re.sub(checkalignpattern, r'\n\\end{align}', content)

    #{align*}
    alignstarpattern = re.compile(r'\\begin{(align\*)}(.*?)\n\\end{align\*}', re.DOTALL)
    content = re.sub(alignstarpattern, replacestar, content)
    
    return content
