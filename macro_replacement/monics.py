import re
import sys

global fullmacro
fullmacro = ''

def main():

    #input from command line
    if len(sys.argv) != 3:
        print("Usage: programname.py inputfile outputfile")
        sys.exit()

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    file = open(inputfile, 'r')
    content = file.read()

    content = replace_monics(content)

    #writes output
    file = open(outputfile, 'w')
    file.write(content)
    file.close()

def replace_monics(content):

    monic_file = open('monic_names', 'r').read()

    global names 
    names = {}
    name_pat = re.compile(r'section{(.*?)}\s(.+)')
    
    lines = monic_file.split('\n')
    for line in lines:
        if len(name_pat.findall(line)) > 0:
            list = name_pat.findall(line)[0]
            names[list[0]] = (list[1]).strip()
                
    drmf = open('./DRMFfcns.sty', 'r').read()
    dlmf = open('./DLMFfcns.sty', 'r').read()
    
    global drmfdlmf
    drmfdlmf = drmf + dlmf
    
    KLS_pat = re.compile(r'section{([^\n]+)}\n(.+?){Symmetry}', re.DOTALL)
    content = KLS_pat.sub(rpl_section, content)

    section_pat = re.compile(r'section{(.+?)}(.+?)\\subsection\*{Reference', re.DOTALL)
    content = section_pat.sub(rpl_section, content)
    
    return content

def rpl_section(match):

    section_n = match.group(1)
    macro_n = names[section_n] # holds current macro name only
    matchstr = match.group(0)
    
    params = 0
    args = 0
    dlmf_pat = re.compile(r'\\defSpecFun{' + macro_n + '}\[(\d)\].+?\[meaning=.+?\]{(\d)}')
    if len(dlmf_pat.findall(drmfdlmf)) > 0:
        list = dlmf_pat.findall(drmfdlmf)[0]
        params = int(list[0])
        args = int(list[1])

    if args == 0 and params == 0:
        # special case for chebyU and chebyT
        hyper_pat = re.compile(r'{Normalized recurrence relations}(.+?)\\subsection', re.DOTALL)
        matchstr = hyper_pat.sub(cheby_case_helper, matchstr)
        return matchstr

    # generates string for pattern matching
    p = '({|\[)([^=_;,|$]+?)(}|\])'
    a = '({)([^=_;,|$]+?)(})'
    global macro_regex
    macro_regex = macro_n
    macro_regex = macro_regex + ''.join([p for s in range(params)])
    macro_regex = macro_regex + '@'
    macro_regex = macro_regex + ''.join([a for s in range(args)])
    macro_regex = macro_regex + '(?!})'

    hyper_pat = re.compile(r'{Normalized recurrence relation}(.+?)\\subsection', re.DOTALL)
    hyper_pat.sub(find_name, matchstr)

    monic_pat = re.compile(r'p_(?P<open>{)?([^=_;,|$]+?)(?(open)})\(([^=_;,|$]+?)\)(?!\))')
    matchstr = monic_pat.sub(make_monic, match.group(0))

    return matchstr

def find_name(match):

    matchstr = match.group(0)
    macro_pat = re.compile(macro_regex) 
    
    macro_pat.sub(find_args, matchstr)
    return

def find_args(match):

    global fullmacro
    fullmacro = '\\monic' + match.group(0) 
    return

def make_monic(match):

    before_m = fullmacro.split('@')[0]
    before_m = before_m[:before_m.rfind('{')]
    after_m = fullmacro.split('@')[1]    
    
    if after_m.find('}{') != -1:
        after_m = after_m[after_m.find('}{') + 1:]
    else:
        after_m = ""

    output = before_m + '{' + match.group(2) + '}@@{' + match.group(3) + '}' + after_m
    return output

def cheby_case_helper(match):
    
    cheby_pat = re.compile(r'\\begin{equation}(.+?)\\end{equation}\nwhere(.+?)\n', re.DOTALL)
    matchstr = cheby_pat.sub(cheby_case, match.group(0))
    return matchstr

    
def cheby_case(match):

    m = ''

    if 'ChebyT' in match.group(0):
        m = 'ChebyT'

    elif 'ChebyU' in match.group(0):
        m = 'ChebyU'

    monic_pat = re.compile(r'p_(?P<open>{)?([^=_;,|$]+?)(?(open)})\(([^=_;,|$]+?)\)')
    matchstr = monic_pat.sub('\\monic' + m + '{\g<2>}@@{\g<3>}', match.group(0))
    return matchstr


if __name__ == '__main__':
    main()
