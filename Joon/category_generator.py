#!/usr/bin/env python
import os

names = ["BS", "CH", "CN", "EF", "ER", "EX", "GA", "HY", "QH", "SM"]
name_dictionary = {'naturallogarithm': 'naturallogarithm', 'archimedes': 'archimedes', 'arcsinh': 'arcsinh',
                   'pow': 'pow', 'fresnel': 'fresnel', 'modbessel': 'Modified Bessel functions', 'apery': 'apery',
                   'arccos': 'arccos', 'HY': 'HY', 'BS': 'Bessel', 'tan': 'tan', 'GA': 'GA', 'gamma_chisquare':
                       'gamma_chisquare', 'powerandroot': 'powerandroot', 'error': 'error', 'gompertz': 'gompertz',
                   'ln': 'ln', 'kummer': 'kummer', 'whittaker': 'whittaker', 'arctan': 'arctan', 'trigamma': 'trigamma',
                   'eulersconstant': 'eulersconstant', 'binet': 'binet', 'parabolic': 'parabolic', 'repint': 'repint',
                   'bessel': 'Bessel functions', 'sin': 'sin', 'incompletegamma': 'incompletegamma', 'CH': 'CH',
                   'pythagoras': 'pythagoras', 'CN': 'CN', 'normal': 'normal', 'arcsin': 'arcsin',
                   'confluentlimit': 'confluentlimit', 'confluent': 'confluent', 'eulersnumber': 'eulersnumber',
                   'catalan': 'catalan', 'repeated': 'repeated', 'arctanh': 'arctanh', 'EX': 'EX', 'rabbit': 'rabbit',
                   'QH': 'QH', 'beta_f_t': 'beta_f_t', 'cosh': 'cosh', 'coth': 'coth', 'ER': 'ER', 'sinh': 'sinh',
                   'cos': 'cos', 'SM': 'SM', 'EF': 'EF', 'tanh': 'tanh', 'expintegrals': 'expintegrals', 'polygamma':
                       'polygamma', 'exp': 'exp', 'goldenratio': 'goldenratio', 'comperror': 'comperror', 'arccosh':
                       'arccosh', 'tetragamma': 'tetragamma', 'related': 'related', "": ""}


def generate_categories():
    """
    Generates section, subsection
    """

    root_directory = "/home/jnb8/CFSF/functions"
    depth = len(root_directory.split("/"))

    dirs = [x for x in os.walk(root_directory)]

    sections_created = list()
    # current_section = ""
    text = ""

    # print name_dictionary

    other_text = ""
    subsections = {"no-subsection": list()}
    for i in range(len(dirs)+1):
        if i < len(dirs):
            d = dirs[i]
        else:
            d = [root_directory, [], []]

        if "/functions/" in d[0]:  # only subdirectories of functions/
            print str(d)
            other_text += d[0].split("/")[-1]+"\n"
            # so the first one will be the list of "names"
            section = d[0].split("/")[depth]  # should be in names

            if len(d[0].split("/")) == depth+1 or i == len(dirs):  # switched to a new section
                # print "Switched to new section"
                for qq in subsections:
                    thing = subsections[qq]
                    if not thing and qq == "no-subsection":
                        pass
                    else:
                        text += "  \\subsection{"+qq+"}\n"
                        for j in thing:
                            text += "    "+j+"\n"
                        text += "\n"

                subsections = {"no-subsection": list()}

            if section not in sections_created:
                text += "\\section{"+name_dictionary[section]+"}\n"
                sections_created.append(section)

            for thing in d[1]:
                subsections[name_dictionary[thing]] = list()

            for thing in d[2]:
                if len(d[0].split("/")) == depth+1:
                    subsections["no-subsection"].append(thing)
                else:
                    subsections[name_dictionary[d[0].split("/")[depth+1]]].append(thing)

    # maybe write some better code.
    print '\n'.join(text.split("\n")[:-2]).replace("  \subsection{no-subsection}\n  ", "")

    print other_text


def main():
    generate_categories()

if __name__ == '__main__':
    main()
