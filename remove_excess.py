"""This program begins with an unprocessed LaTeX file and removes parts that are unnecesssary for the DLMF."""

import re
import sys

import parentheses
from utilities import (writeout, readin, get_line_lengths,
    find_line)

EQ_START = r'\begin{equation}'
EQ_END = r'\end{equation}'

CASES_START = r'\begin{cases}'
CASES_END = r'\end{cases}'

EQMIX_START = r'\begin{equationmix}'
EQMIX_END = r'\end{equationmix}'

STD_REGEX = r'.*?###open_(\d+)###.*?###close_\1###'

def main():

    if len(sys.argv) != 3:

        fname = "ZE.tex"
        dot_ind = fname.index(".") + 1 
        ofname = fname[:dot_ind] + "1." + fname[dot_ind:]

    else:

        fname = sys.argv[1]
        ofname = sys.argv[2]   

    writeout(ofname, remove_excess(readin(fname)))

def remove_group(name, content, skip_lines):
    """Removes the group bounded by the group name and then curly braces."""
    
    str_pat = name + STD_REGEX
    pattern = re.compile(str_pat, re.DOTALL)

    return pattern.sub(r'', content)

def remove_section(start, end, content):
    """Removes the section or part bounded by start and end."""
    
    str_pat = start + r'.*?(' + end + r')'
    pattern = re.compile(str_pat, re.DOTALL) 

    return pattern.sub(r'\1', content)

def remove_begin_end(name, content):
    """Removes a group bound by \\begin{name} and \\end{name}."""

    str_pat = r'\\begin{' + name + r'}.*?\\end{' + name + r'}'
    pattern = re.compile(str_pat, re.DOTALL)

    return pattern.sub(r'', content)

def remove_excess(content):
    """Removes the excess pieces from the given content and returns the updated version as a string."""

    oldest = content

    updated = _get_preamble()
    old = content

    #edit single lines
    content = re.sub(r'\\bibliography{\.\./bib/DLMF}', r'\\bibliographystyle{plain}' + "\n" + r'\\bibliography{/home/hcohl/DRMF/DLMF/DLMF.bib}', content)
    content = re.sub(r'\\author\[.*?\]{(.*?)}', r'\\author{\1}', content) 
    content = re.sub(r'{math}', r'{equation}', content)
   
    #modify labels, etc
    content = re.sub(r'\\begin{equation}\[.*?\]+', r'\\begin{equation}', content, re.DOTALL)

    print(len(old) -len(content))
    old = content
    
    #remove from something to the start of the next section/part/etc
    content = remove_section(r'\\section{Special Notation}', r'\\part', content)
    content = remove_section(r'\\part{Computation}', r'\\bibliographystyle{plain}', content)
    content = remove_section(r'\\part{References}', r'\\bibliographystyle{plain}', content)
    content = remove_section(r'\\section{Graphics}', r'\\section', content)
    content = remove_section(r'\\section{Graphics}', r'\\section', content)
    content = remove_section(r'\\subsection{Graphics}', r'\\subsection', content)
    content = remove_section(r'\\section{Integrals}', r'\\section', content)
    content = remove_section(r'\\subsection{Integrals}', r'\\subsection', content)
    content = remove_section(r'\\section{Physical Applications}', r'\\bibliographystyle{plain}', content) 

    print(len(old) - len(content))
    old = content

    to_join = []

    #takes out comment lines first
    for line in content.split("\n"):
        
        #if line only consists of % replace with nothing, otherwise don't add back
        if line.lstrip().startswith("%"):
            if line.rstrip().endswith("%"):
                line = ""
            else:
                continue

        to_join.append(line)

    content = "\n".join(to_join)

    skip_lines = set()

    #remove begin/end groups
    content = remove_begin_end("figuregroup", content)
    content = remove_begin_end("comment", content)
    content = remove_begin_end("figure", content)
    content = remove_begin_end("errata", content)

    content = parentheses.remove(content, curly=True)    

    to_remove = [
        r'\\citet',
        r'\\lxDeclare\[.*?\]', 
        r'\\note',
        r'\\origref',
        r'\\lxRefDeclaration',
        r'\\MarkDefn.*?###open_(\d+)###.*?###close_\1###',
        r'\\indexdefn', 
        r'\\MarkNotation.*?###open_(\d+)###.*?###close_\1###',
        r'\\affiliation', 
    ]

    lengths = get_line_lengths(content)

    #go through each group and remove it
    for name in to_remove:
        
        str_regex = name + STD_REGEX
        pattern = re.compile(str_regex, re.DOTALL)

        #go through every match, finding start and end
        for match in pattern.finditer(content):

            group = match.group()

            start = find_line(match.start(), lengths)
            end = find_line(match.end(), lengths)         

            #print("{0}: {1} - {2}".format(group, start, end))

            skip_lines.update(range(start, end + 1)) 

    #define items that cannot be at the beginning of any line or be contined in any line
    illegal_starts = [r'\documentclass{DLMF}', r'\thischapter', r'\part{Notation}', r'\begin{equationgroup', r'\end{equationgroup', r'\begin{onecolumn', r'\end{onecolumn']
    illegal_elements = [r'TwoToOneRule', r'OneToTwoRule', r'\citet']

    lines = content.split("\n")

    #various flags that will be useful when going through the lines
    in_eq = False
    in_eqmix = False
    in_const = False
    in_cases = False

    eqmix_label = ""
    const_str = ""

    #remove trailing % and whitespace and add to updated - also remove lines that should be skipped
    for lnum, line in enumerate(lines):

        lnum += 1

        #don't add line back if it should be skipped
        if lnum in skip_lines:
            continue
         
        line = parentheses.insert(line, curly=True)
        line_checks = [line.lstrip().startswith(start) for start in illegal_starts] + [element in line for element in illegal_elements] 
        
        #skip current line if it starts with or contains an illegal element
        if any(line_checks):
            continue 

        cleaned = line.rstrip().rstrip("%").rstrip()

        #line marks the start of an equationmix, set the flag and remove the line
        if EQMIX_START in cleaned:
            in_eqmix = True
            eqmix_label = cleaned[cleaned.index(r'\label'):] 
            continue

        #line marks the end of an equationmix, set the flag and remove the line
        if EQMIX_END in cleaned:
            in_eqmix = False
            eqmix_label = ""
            continue

        #if this line marks the start of an equation, set the flag
        if EQ_START in cleaned:
            in_eq = True 
            cleaned = cleaned + eqmix_label
        
        #if this line marks the end of an equation, set the flag
        if EQ_END in cleaned:
            in_eq = False

        #comment out constraints and replace commas with double commas; we need to build the entire constraint string and then add it back together
        if cleaned.lstrip().startswith(r"\constraint"):
            in_const = True

        #starting a cases statement
        if CASES_START in cleaned:
            in_cases = True

        #ending a cases statement
        if CASES_END in cleaned:
            in_cases = False

        #remove commas, periods, colons, and semi-colons from the end of equations
        if in_eq and not in_const:
            to_strip = ":;,"
             
            #don't take off trailing commas when in a cases block
            if in_cases:
                to_strip = to_strip[:-1]
               
            cleaned = cleaned.rstrip(to_strip)

        #we're still in a constraint, replace commas and comment out
        if in_const:

            const_str += cleaned

            #we're done with the constraint, make substitutions
            if cleaned.rstrip().rstrip(".,").endswith("}"):

                const_str = re.sub(r'\$[;,](\s*(?:\$|or))', r'$ &\1', const_str)                  
                in_const = False
            
                #constraint ends with two }, put one on next line
                if cleaned.rstrip().endswith("}}"):
                    const_str = const_str[:-1] + "\n}"
                 
                const_lines = []
                split = const_str.split("\n")
                
                offset = 1

                #account for the case when there are no newlines present
                if len(split) == 1:
                    offset = 0 

                #split multiline constraints back into multiple lines
                for const_line in split[offset:]:
                  
                    #if line is not just a bracket, comment it out
                    if const_line.strip() != "}":
                        const_line = "%" + const_line
                    
                    const_lines.append(const_line)

                updated.extend(const_lines)
                const_str = ""

            const_str += "\n"

            continue

        updated.append(cleaned)

    content = '\n'.join(updated)

    #remove blank lines around begin and end equation
    space_pat = re.compile(r'\\begin{equation}(.*?)$\s+$', re.MULTILINE)
    content = space_pat.sub(r'\\begin{equation}\1', content)

    space_pat = re.compile(r'^\s*$\n\\end{equation}', re.MULTILINE)
    content = space_pat.sub(r'\\end{equation}', content)

    #remove consecutive blank lines
    content = re.sub(r'(\n){3,}', '\n\n', content)

    print("Final: {0}".format(len(oldest) - len(content)))

    return content

#returns the preamble as a list of it's lines
def _get_preamble():

    preamble = []

    preamble.append('\\documentclass{article}')
    preamble.append('\\usepackage{amsmath}')
    preamble.append('\\usepackage{amsfonts}')
    preamble.append('\\usepackage{breqn}')
    preamble.append('\\usepackage{DLMFmath}')
    preamble.append('\\usepackage{DRMFfcns}')
    preamble.append('')
    preamble.append('\\oddsidemargin -0.7cm')
    preamble.append('\\textwidth 18.3cm')
    preamble.append('\\textheight 26.0cm')
    preamble.append('\\topmargin -2.0cm')
    preamble.append('')
    preamble.append('%  \constraint{')
    preamble.append('%  \substitution{')
    preamble.append('%  \drmfnote{')
    preamble.append('%  \drmfname{')
    preamble.append('')

    return preamble

if __name__ == "__main__":
    main()
