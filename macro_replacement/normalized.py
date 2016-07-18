import re
import sys
from snippets import *

def main():

    #input from command line
    if len(sys.argv) != 3:
        print('Usage: programname.py inputfile outputfile')
        sys.exit()

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    file = open(inputfile, 'r')
    content = file.read()

    content = replace_normalized(content)

    #writes output
    file = open(outputfile, 'w')
    file.write(content)
    file.close()

def replace_normalized(content):

    normalized_file = open('normalized_names', 'r').read()

    global names
    names = {}
    name_pat = re.compile(r'section{(.*?)}\s(.+)')
    
    lines = normalized_file.split('\n')
    for line in lines:
        if len(name_pat.findall(line)) > 0:
            list = name_pat.findall(line)[0]
            names[list[0]] = (list[1]).strip()

    KLS_pat = re.compile(r'()section{([^\n]+)}\n(.+?){Symmetry}', re.DOTALL) #TODO: add recurrence relation
    content = KLS_pat.sub(rpl_section, content)

    section_pat = re.compile(r'(section{(.+?)}.+?{Orthogonality relation})(.+?\\subsection\*{Recurrence relation}.+?)(\\subsection)', re.DOTALL)
    content = section_pat.sub(rpl_section, content)

    section_pat = re.compile(r'(section{(.+?)}.+?{Orthogonality relation})(.+?)(\\subsection)', re.DOTALL)
    content = section_pat.sub(rpl_section, content)

    section_pat = re.compile(r'(section{(.+?)}.+?{Recurrence relation})(.+?)(\\subsection)', re.DOTALL)
    content = section_pat.sub(rpl_section, content)

    return content

def rpl_section(match):

    section_n = match.group(2)
    search_in = match.group(3)
    matchstr = match.group(0)

    # pattern for finding correct name of macro
    full_rpl_pat = re.compile(r'where\n.*?\n*.*?:=(.+?)(?:=|\$)')
    if len(full_rpl_pat.findall(search_in)) == 0 or section_n not in names:
        # correct macro name not found
        return matchstr

    macro_pat = names[section_n] # holds current pattern

    # extracts macro name
    global full_macro
    templist = full_rpl_pat.findall(search_in)
    for i in range(len(templist)):
        full_macro = full_rpl_pat.findall(search_in)[i]
        if full_macro.endswith(r'.'):
            full_macro = full_macro[:-1]
        #print('{0:20} {1}'.format(section_n, full_macro))
        if r'@' in full_macro:
            break

    full_macro = full_macro.replace(r'@', r'@@')

    # makes replacements in section
    normalized_pat = re.compile(macro_pat)
    search_in = normalized_pat.sub(replace_macro, search_in)
    #print(search_in)

    return match.group(1) + search_in + match.group(4)

def replace_macro(match):

    before_m = full_macro[:full_macro.find('{') + 1]
    after_m = full_macro[full_macro.find('}'):]

    return before_m + match.group(2) + after_m

if __name__ == '__main__':
    main()
