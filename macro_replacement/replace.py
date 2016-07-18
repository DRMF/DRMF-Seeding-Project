#!/usr/bin/python
"""This module contains the code for the 'replace' functionality of the DRMF seeding program."""

import identifiers
import sys
import re
import os
from snippets import *
from function import Function
from replace_special import remove_special
from monics import replace_monics
from normalized import replace_normalized
from cosSubstitution import cos_substitution

#Changes the '\mid ' to '|' and '\half' to '\frac{1}{2}'
def replace_basic(content):

    content = content.replace(r'\mid q', '|q')
    content = content.replace(r'\half', r'\frac{1}{2}')
    
    return content

#go through input file and make replacements specified
def replace_all(content, all_funcs):

    #perform replacement using each imported module
    for func in all_funcs:
        content = func.make_subs(content)

    return content

def run(inputfile, outputfile, all_funcs):
    """Reads in content from inputfile, performs replacement for every function provided, and writes results to outputfile."""

    file = open(inputfile,"r")
    content = file.read()

    #Header replacements
    content = content.replace(r'\usepackage{amssymb}', '\\usepackage{amsfonts}\n%\\usepackage{breqn}\n\\usepackage{DLMFmath}\n\\usepackage{DRMFfcns}\n\\usepackage{amssymb}')
    content = replace_basic(content)
    #content = identifiers.LabelAll(content, all_funcs)

    #Makes replacements
    content = replace_all(content, all_funcs)
    content = replace_monics(content)
    content = replace_normalized(content)
    content = remove_special(content)
    content = cos_substitution(content)

    #Writes the converted string into the output file
    file2 = open(outputfile,"w")
    file2.write(content)
    file2.close()
