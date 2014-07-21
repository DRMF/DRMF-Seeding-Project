"""
Prepare the special annotations in the file by uncommenting them and further
readying them to be converted to WikiText.

Special Annotations
===================

The Special Annotations are:

*``\constraint``
*``\substitution``
*``\drmfnote``
*``\drmfname``
*``proof``
"""

import re
import sys

import parentheses
from utilities import (readin, writeout, remove_inner_whitespace,
    get_line_lengths, find_line)    

FLUSH_START = r'\begin{flushright}'
FLUSH_END = r'\end{flushright}'

ANNOTATION_STR = r'\s*%\s*\\(?:constraint|substitution|drmf(?:note|name)|proof)'
ANNOTATION_PAT = re.compile(ANNOTATION_STR, re.MULTILINE)

BRACE_PAT = re.compile(r'(?P<annotation>' + ANNOTATION_STR + r')###open_(\d+)###(?![$ ])(?P<content>.*?)(?![$ ])###close_\2###', re.DOTALL)

MEASURE_PAT = re.compile(r'(\S)\\\\\[0.2cm\]')

def main():

    #get the names of the input and output files
    if len(sys.argv) != 3:

        fname = "ZE.3.tex"
        ofname = "ZE.4.tex"

    else:

        fname = sys.argv[1]
        ofname = sys.argv[2]   

    writeout(ofname, prepare_annotations(readin(fname)))

def prepare_annotations(content):
    """
    Prepares annotations in `content` to be compatible with WikiText.

    Transformations include:
       * uncommenting
       * special formatting
       * etc.
    """
    
    docstart = content.find(r'\begin{document}')

    eq_comment_pattern = re.compile(r'\\begin{equation}(?P<before>\\label{(?P<eq_label>.*?)}.*?\n^[^%]*$)(?P<comment>\n^ *%[\w\s\\{}()<>[\]&=@%,.:;|\'~_^$/+-]*?\n)\\end{equation}', re.MULTILINE)

    content = content[:docstart] + eq_comment_pattern.sub(replace_comments, content[docstart:])


    special_annotations = {
        r'\\constraint': "C",
        r'\\substitution': "S",
        r'\\drmfnote': "NOTE",
        r'\\drmfname': "NAME",
        r'\\proof': "PROOF"
    }

    #replace the annotations with their "code"
    for annotation, code in special_annotations.iteritems():
        content = content[:docstart] + re.sub(annotation, r'{\\bf ' + code + '}:~', content[docstart:])

    content = content.replace("~{", "~")
    content = content.replace("~ ", "~")

    content = content.replace("&", r"\&")

    return content

#moves annotations from inside equation blocks to the end of them and wraps them in a flushright block
def replace_comments(match):
    """
    Processes each equation block that contains comments.

    Given the whole block, it returns the processed block, which has
    all comments uncommented and placed in a flushright block after
    the equation block.

    Sample:::

        \\begin{equation}\\label{eq:ZE.EX.ZE5}
            \\RiemannZeta'@{s} = - \\sum_{n=2}^\\infty (\\ln@@{n}) n^{-s}
            %  \\constraint{$\\realpart{s} > 1$}
        \\end{equation}
 
    becomes::

        \\begin{equation}\\label{eq:ZE.EX.ZE5}
            \\RiemannZeta'@{s} = - \\sum_{n=2}^\\infty (\\ln@@{n}) n^{-s}
        \\end{equation}
        \\begin{flushright}
            {\\bf C}:~${\\displaystyle \\realpart{s} > 1}$
        \\end{flushright}
    """

    before = match.group("before")

    #print("Equation label: {0}".format(match.group("eq_label")))

    replacement = r'\begin{equation}' + before

    comment = match.group("comment")

    updated = []
    add_measure = False

    total_annotations = len(re.findall(r'\n' + ANNOTATION_STR, comment))
    annotations_left = total_annotations

    prev_annotations = 0

    comment = parentheses.remove(comment, curly=True)
    comment = BRACE_PAT.sub(r'\g<annotation>\g<content>', comment)
    comment = parentheses.insert(comment, curly=True)

    #make sure every line in the comment is actually a comment
    for comment_line in comment.split("\n"):

        stripped = comment_line.lstrip()

        #line isn't really a comment, add it back to the equation
        if not stripped.startswith("%"):
            replacement += comment_line + "\n"
 
        else:        #otherwise, process it (take off % and add in \displaystyle) and add it to the comment

            num_annotations = len(ANNOTATION_PAT.findall(comment_line))

            #add measurement to the previous line if the current line is starting a new annotation
            add_measure = num_annotations and annotations_left != total_annotations

            annotations_left -= num_annotations
 
            leading_whitespace = len(comment_line) - len(stripped) + 1
            comment_line = " " * leading_whitespace + stripped.lstrip("%") 

            old_len = len(comment_line)

            comment_line = re.sub(r'\$\s*}', r'$}', comment_line)
            comment_line = re.sub(r'{\s*\$', r'{$', comment_line)

            extra_whitespace = old_len != len(comment_line)

            first_brack = comment_line.find("{")

            #if we're going to go out of bounds, nothing to do on this line
            if first_brack + 1 < len(comment_line):
                after_first = comment_line[first_brack + 1]
            else:
                continue
           
            dollar_locs = _get_dollar_locs(comment_line)

            offset = 0

            #there's at least one $ in the line
            while dollar_locs:
 
                #the $ are balanced
                if len(dollar_locs) % 2 == 0:
       
                    dollar_iter = iter(dollar_locs)

                    start, end = (dollar_iter.next(), dollar_iter.next())

                    previous = ""
                    disp_string = '${' + r'\displaystyle '

                    #only try to look behind the $ if it isn't the first character in the line
                    if start != 0:
                        previous = comment_line[start-1]
 
                    #we may need to add a space before displaystyle
                    if previous == " ":
                        disp_string = " " + disp_string

                    comment_line = comment_line[:start] + " " * extra_whitespace + disp_string + comment_line[start + 1:end] + '}' + comment_line[end:]
                    comment_line = comment_line.rstrip().rstrip("}") + " "

                dollar_locs = _get_dollar_locs(comment_line)
                offset += 2

                dollar_locs = dollar_locs[offset:]

            #add the measurement at the end
            if add_measure:
                last = updated[-1] 
                last += r'\\[0.2cm]'
                last = MEASURE_PAT.sub(r'\1 \\\\[0.2cm]', last)
                updated[-1] = last

            prev_annotations = num_annotations

            comment_line = remove_inner_whitespace(comment_line)
            comment_line = comment_line.rstrip()
            updated.append(comment_line)

    comment = "\n" + "\n".join(updated) + "\n"

    comment = comment.replace("$}", "$")
    comment = comment.replace("{$", "$")

    replacement = replacement[:-1]
    replacement += r'\end{equation}' + "\n" + r'\begin{flushright}'

    replacement += comment

    replacement += r'\end{flushright}'

    #print("")
    return replacement

#returns a list of the locations of the $ in the given string
def _get_dollar_locs(words):

    locs = []

    start = 0

    next_loc = words.find("$", start)

    #keep adding to the list as long as more $ remain
    while next_loc != -1:
        locs.append(next_loc)
        start = next_loc + 1
        next_loc = words.find("$", start)

    return locs

#call main function
if __name__ == "__main__":
    main()
