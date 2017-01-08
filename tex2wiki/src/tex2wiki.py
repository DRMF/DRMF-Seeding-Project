__author__ = "Joon Bang"
__status__ = "Prototype"

INPUT_FILE = "tex2wiki/data/09outb.tex"
OUTPUT_FILE = "tex2wiki/data/09outb.mmd"
GLOSSARY_LOCATION = "tex2wiki/data/new.Glossary.csv"
TITLE_STRING = "Orthogonal Polynomials"
METADATA_TYPES = ["substitution", "constraint"]
METADATA_MEANING = {"substitution": "Substitution(s)", "constraint": "Constraint(s)"}

import copy
import compare_files
import csv


class LatexEquation(object):
    def __init__(self, label, equation, metadata):
        self.label = label
        self.equation = equation
        self.metadata = metadata

    def __str__(self):
        return self.label + "\n" + self.equation + "\n" + str(self.metadata)

    @staticmethod
    def make_from_raw(raw):
        equations = raw[:-1]
        for i, equation in enumerate(equations):
            # formula stuff
            try:
                formula = format_formula(get_data_str(equation, latex="\\formula"))
            except IndexError:  # there is no formula.
                break

            equation = equation.split("\n")

            # get metadata
            raw_metadata = ""

            j = 0
            while j < len(equation):
                if "%" in equation[j]:
                    raw_metadata += equation.pop(j)[1:].strip().strip("\n") + "\n"
                else:
                    j += 1

            metadata = dict()
            for data_type in METADATA_TYPES:
                temp = format_metadata(get_data_str(raw_metadata, latex="\\" + data_type)).split("\n")
                for k, line in enumerate(temp):
                    if line.rstrip().endswith("&"):
                        temp[k] = line.rstrip() + "<br />"

                metadata[data_type] = "\n".join(temp)

            equations[i] = LatexEquation(formula, '\n'.join(equation), metadata)

        return equations


class FormattedEquation(object):
    def __init__(self, label, equation, metadata):
        self.label = label
        self.equation = equation
        self.metadata = metadata

    def __str__(self):
        return "Equation: " + self.equation + "\nMetadata: " + ("empty\n" if self.metadata == "" else self.metadata)


class DataUnit(object):
    def __init__(self, title, subunits):
        self.title = title
        self.subunits = subunits

    def __str__(self):
        result = self.title + "\n"

        if type(self.subunits) == list and len(self.subunits) and type(self.subunits[0]) == DataUnit:
            for sub in self.subunits:
                result += str(sub) + "\n"
        else:
            result += str("\n".join([str(eq) for eq in self.subunits])) + "\n"

        return result


def generate_html(tag_name, text, options=None, spacing=2):
    # type: (str, str(, dict, bool)) -> str
    """
    Generates an html tag, with optional html parameters.
    When spacing = 0, there should be no spacing.
    When spacing = 1, the tag, text, and end tag are padded with spaces.
    When spacing = 2, the tag, text, and end tag are padded with newlines.
    """
    if options is None:
        options = {}

    option_text = [key + "=\"" + value + "\"" for key, value in options.iteritems()]
    result = "<" + tag_name + " " * (option_text != []) + ", ".join(option_text) + ">"

    if spacing == 2:
        result += "\n" + text + "\n</" + tag_name + ">\n"
    elif spacing == 1:
        result += " " + text + " </" + tag_name + ">"
    else:
        result += text + "</" + tag_name + ">"

    return result


def generate_math_html(text, options=None, spacing=2):
    # type: (str(, dict, int)) -> str
    """Special case of generate_html, where the tag is "math"."""
    if options is None:
        options = {}

    option_text = [key + "=\"" + value + "\"" for key, value in options.iteritems()]
    result = "<math" + " " * (option_text != []) + ", ".join(option_text) + ">"

    if spacing == 2:
        result += "{\\displaystyle \n" + text + "\n}</math>\n"
    elif spacing == 1:
        result += "{\\displaystyle " + text + "}</math>\n"
    else:
        result += "{\\displaystyle " + text + "}</math>"

    return result


def generate_link(left, right=""):
    # type: (str(, str)) -> str
    """Generates a MediaWiki link."""
    if right == "":
        return "[[" + left + "|" + left + "]]"

    return "[[" + left + "|" + right + "]]"


def multi_split(s, seps):
    # type: (str, list) -> list
    """Splits a string on multiple characters."""
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res


def convert_dollar_signs(string):
    # type: (str) -> str
    """Converts dollar signs to html for math mode."""
    count = 0
    result = ""
    for i, ch in enumerate(string):
        if ch == "$":
            if count % 2 == 0:
                result += "<math>{\\displaystyle "
            else:
                result += "}</math>"
            count += 1
        else:
            result += ch

    return result


def format_formula(formula):
    if formula[0] == ":":
        return formula[1:].zfill(2)

    formula = multi_split(formula.split("Formula:", 1)[1], [".", ":"])

    for j in [-1, -2, -3]:
        formula[j] = formula[j].zfill(2)

    if len(formula) == 3:
        formula = formula[0] + "." + formula[1] + ":" + formula[2]
    else:
        formula = ":".join(formula[:-3]) + ":" + formula[-3] + "." + formula[-2] + ":" + formula[-1]

    return formula


def format_metadata(string):
    # type: (str) -> str
    """Formats the metadata of an equation."""
    if string == "":
        return ""

    # modified convert_dollar_sign algorithm
    dollar_count = 0
    result = ""
    for i, ch in enumerate(string):
        if ch == "$":
            if dollar_count % 2 == 1:
                result += "}</math>"
            elif dollar_count > 1:
                result = result[:-1] + "<br />\n<math>{\\displaystyle "
            else:
                result += "<math>{\\displaystyle "
            dollar_count += 1
        else:
            result += ch

    return result.strip()


def extract_data(data):
    # type: (list) -> list
    """Extracts the equations and pertinent data from the tex file."""
    result = list()

    for section_data in data:
        equations = section_data[1][:-1]
        for i, equation in enumerate(equations):
            # formula stuff
            try:
                formula = format_formula(get_data_str(equation, latex="\\formula"))
            except IndexError:  # there is no formula.
                break

            equation = equation.split("\n")

            # get metadata
            raw_metadata = ""

            j = 0
            while j < len(equation):
                if "%" in equation[j]:
                    raw_metadata += equation.pop(j)[1:].strip().strip("\n") + "\n"
                else:
                    j += 1

            metadata = dict()
            for data_type in METADATA_TYPES:
                metadata[data_type] = format_metadata(get_data_str(raw_metadata, latex="\\"+data_type))

            equations[i] = LatexEquation(formula, '\n'.join(equation), metadata)

        result.append([section_data[0], equations])

    return result


def find_end(text, left_delimiter, right_delimiter, start=0):
    # type: (str, str, str(, int)) -> int
    """A .find that accounts for nested delimiters."""
    net = 0  # left delimiters encountered - right delimiters encountered
    for i, ch in enumerate(text[start:]):
        if ch == left_delimiter:
            net += 1
        elif ch == right_delimiter:
            if net == 1:
                return i + start
            else:
                net -= 1

    return -1


def get_data_str(text, latex=""):
    # type: (str(, str)) -> str
    """Gets the string in between curly brackets."""
    start = text.find(latex + "{")

    if start == -1:
        return ""

    return text[start + len(latex + "{"):find_end(text, "{", "}", start)]


def generate_nav_bar(info):
    # type: (list) -> list
    """Generates the navigation bar code for a page."""
    links = list()
    for link, text in info:
        link = link.replace("''", "")
        text = text.replace("''", "")
        links.append(generate_link(link, text))

    nav_section = generate_html("div", "<< " + links[0], options={"id": "alignleft"}, spacing=1) + "\n" + \
        generate_html("div", links[1], options={"id": "aligncenter"}, spacing=1) + "\n" + \
        generate_html("div", links[2] + " >>", options={"id": "alignright"}, spacing=1)

    header = generate_html("div", nav_section, options={"id": "drmf_head"})
    footer = generate_html("div", nav_section, options={"id": "drmf_foot"})

    return header, footer


def get_macro_name(macro):
    # type: (str) -> str
    """Obtains the macro name."""
    macro_name = ""
    for ch in macro:
        if ch.isalpha() or ch == "\\":
            macro_name += ch
        elif ch in ["@", "{", "["]:
            break

    return macro_name


def find_all(pattern, string):
    # type: (str, str) -> generator
    """Finds all instances of pattern in string."""

    i = string.find(pattern)
    while i != -1:
        yield i
        i = string.find(pattern, i + 1)


def get_symbols(text, glossary):
    # type: (str, dict) -> str
    """Generates span text based on symbols present in text. Equivalent of old symbols_list module."""
    symbols = set()

    for keyword in glossary:
        for index in find_all(keyword, text):
            # if the macro is present in the text
            if index != -1:
                index += len(keyword)  # now index of next character
                if index >= len(text) or not text[index].isalpha():
                    symbols.add(keyword)

    span_text = ""
    for symbol in sorted(symbols, key=str.lower):
        links = list()
        for cell in glossary[symbol]:
            if "http://" in cell or "https://" in cell:
                links.append(cell)

        id_link = links[0]
        links = ["[" + link + " " + link + "]" for link in links]

        meaning = list(glossary[symbol][1])

        count = 0
        for i, ch in enumerate(meaning):
            if ch == "$" and count % 2 == 0:
                meaning[i] = "<math>{\\displaystyle "
                count += 1
            elif ch == "$":
                meaning[i] = "}</math>"
                count += 1

        appearance = glossary[symbol][4].strip("$")

        span_text += "<span class=\"plainlinks\">[" + id_link + " <math>{\\displaystyle " + appearance + \
                     "}</math>]</span> : " + ''.join(meaning) + " : " + " ".join(links) + "<br />\n"

    return span_text[:-7]  # slice off the extra br and endline


def create_general_pages(data):
    # type: (DataUnit) -> str
    """Creates the 'index' pages for each section. Corrected for use of DataUnit."""
    ret = ""

    section_names = [TITLE_STRING] + [unit.title for unit in data.subunits] + [TITLE_STRING]

    # deep down, subunits is a list of LatexEquation(s)
    for i, section in enumerate(data.subunits):
        result = "drmf_bof\n'''" + section.title.replace("''", "") + "'''\n{{DISPLAYTITLE:" + section.title + "}}\n"

        # get header and footer
        center_text = (TITLE_STRING + "#").replace(" ", "_") + section.title
        link_info = [[section_names[i], section_names[i]], [center_text, section_names[i + 1]],
                     [section_names[i + 2], section_names[i + 2]]]
        header, footer = generate_nav_bar(link_info)

        result += header + "\n" + general_equation_format(section)[0] + "\n" + footer + "\n" + "drmf_eof\n"

        ret += result

    # post-processing
    ret = ret.replace("\n\n\n", "\n")

    return ret


def format_stuffs(data):
    # type: (DataUnit) -> str
    """Format the equations for the 'general' pages."""

    result = copy.deepcopy(data)

    for i, unit in enumerate(result.subunits):
        if type(unit) == LatexEquation:
            equation = generate_math_html(unit.equation, options={"id": unit.label})
            metadata = list()
            for data_type in sorted(unit.metadata.keys()):
                if unit.metadata[data_type] != "":
                    metadata.append(
                        generate_html("div", METADATA_MEANING[data_type] + ": " + unit.metadata[data_type],
                                      options={"align": "right"}, spacing=0)
                    )

            text = equation.rstrip("\n") + "\n" * bool(len(metadata)) + "<br />\n".join(metadata) + "<br />\n"
            result.subunits[i] = text
        else:
            result.subunits[i] = format_stuffs(result.subunits[i])

    return result


def general_equation_format(data, depth=0):
    # type: (DataUnit) -> str
    """Format the equations for the 'general' pages."""

    border = "=" * (2 + int(depth >= 2))  # '==' when depth < 2; '===' when depth >= 2
    text = "%s %s %s\n\n" % (border, data.title, border)

    contains_deeper_depth = False
    metadata = list()
    for i, unit in enumerate(data.subunits):
        if type(unit) == LatexEquation:
            equation = generate_math_html(unit.equation, options={"id": unit.label})
            metadata = list()
            for data_type in sorted(unit.metadata.keys()):
                if unit.metadata[data_type] != "":
                    metadata.append(
                        generate_html("div", METADATA_MEANING[data_type] + ": " + unit.metadata[data_type],
                                      options={"align": "right"}, spacing=0)
                    )

            text += equation.rstrip("\n") + "\n" * bool(len(metadata)) + "<br />\n".join(metadata) + "<br />\n"
        else:
            contains_deeper_depth = True
            temp = general_equation_format(unit, depth + 1)
            text = text.rstrip("\n") + "\n\n" + temp[0]

            if depth + 1 >= 2 and i == len(data.subunits) - 1 and temp[1]:
                text = remove_break(text)

    if depth < 2 and metadata == list() and not contains_deeper_depth:
        text = remove_break(text)

    return text, metadata == list()


def create_specific_pages(data, glossary):
    # type: (DataUnit, dict) -> str
    """Creates specific pages for each formula. Corrected for use with DataUnit."""

    formulae = [TITLE_STRING] + make_formula_list(data)[:-1] + [TITLE_STRING]

    i = 0
    pages = list()
    for j, unit in enumerate(data.subunits):
        res, i = specific_page_format(unit, unit.title, formulae, glossary, j, i)
        pages += res
        i += 1

    return "\n".join(pages) + "\n"


def make_formula_list(info):
    formulae = list()
    if len(info.subunits) and type(info.subunits[0]) != DataUnit:
        for eq in info.subunits:
            formulae.append("Formula:" + eq.label)
        formulae.append(info.title)
    else:
        for subunit in info.subunits:
            formulae += make_formula_list(subunit)

    return formulae


def specific_page_format(info, title, formulae, glossary, j, i=0):
    pages = list()

    if len(info.subunits) and type(info.subunits[0]) != DataUnit:
        for eq in info.subunits:
            # get header and footer
            center_text = (title + "#" + eq.label).replace(" ", "_")
            middle = "formula in " + title
            link_info = [[formulae[i].replace(" ", "_"), formulae[i]], [center_text, middle],
                         [formulae[i + 2].replace(" ", "_"), formulae[i + 2]]]
            header, footer = generate_nav_bar(link_info)

            # add title of page, navigation headers
            result = "drmf_bof\n'''Formula:" + eq.label + "'''\n{{DISPLAYTITLE:Formula:" + eq.label + "}}\n" + header \
                     + "\n<br />"

            # add formula
            result += generate_html("div", generate_math_html(eq.equation)[:-1], options={"align": "center"},
                                    spacing=0) + "\n\n"

            # add metadata
            for data_type, info in eq.metadata.iteritems():
                if info != "":
                    result += "== " + METADATA_MEANING[data_type] + " ==\n\n"
                    result += generate_html("div", info, options={"align": "left"}, spacing=0) + "<br />\n\n"

            # proof section
            result += "== Proof ==\n\nWe ask users to provide proof(s), reference(s) to proof(s), or further " \
                      "clarification on the proof(s) in this space.\n\n"

            # symbols list section
            result += "== Symbols List ==\n\n"
            result += get_symbols(result, glossary) + "\n<br />\n\n"

            # bibliography section
            result += "== Bibliography==\n\n"  # TODO: Fix typo after feature parity has been met
            result += "<span class=\"plainlinks\">[http://homepage.tudelft.nl/11r49/askey/contents.html " \
                      "Equation in Section 1." + str(j + 1) + "]</span> of [[Bibliography#KLS|'''KLS''']]."  # TODO: FIX

            # end of page
            result += "<br />" + footer + "\ndrmf_eof"
            pages.append(result)

            i += 1
    else:
        for subunit in info.subunits:
            res = specific_page_format(subunit, title, formulae, glossary, j, i)
            pages += res[0]
            i = res[1]

    return pages, i


def remove_break(string):
    while string.rstrip("\n").endswith("<br />"):
        string = string.rstrip("\n")[:-6]

    return string


def rstrip(string, delimiter):
    # type: (str, str) -> str
    """A more intuitive version of rstrip, which simply removes delimiter if it is present."""
    while string.endswith(delimiter):
        string = string[:(-1 * len(delimiter))]

    return string


def section_split(string, sub=0):
    # type: (str) -> DataUnit
    """
    Split string into DataTree objects.
    Will eventually become replacement for large part of main() + extract_data(),
    and should theoretically make the create_general_pages and create_specific_pages methods simpler, faster,
    and able to more easily store all data from the .tex file.
    """

    string = string.split("\\" + sub * "sub" + "section")

    # base case; when depth too far
    if len(string) == 1:
        title = get_data_str(string[0]).replace("$", "''")

        equations = string[0].split("\\end{equation}")
        for i, equation in enumerate(equations[:-1]):
            equations[i] = equation.split("\\begin{equation}", 1)[1].strip()

        equations = LatexEquation.make_from_raw(equations)

        return DataUnit(title, equations)

    chunk_data = list()  # list of DataSection

    for chunk in string[1:]:
        chunk_data.append(section_split(chunk, sub + 1))

    title = get_data_str(string[0]).replace("$", "''")

    return DataUnit(title, chunk_data)


def main():
    with open(INPUT_FILE) as input_file:
        text = input_file.read()

    glossary = dict()
    with open(GLOSSARY_LOCATION, "rb") as csv_file:
        glossary_file = csv.reader(csv_file, delimiter=',', quotechar='\"')
        for row in glossary_file:
            glossary[get_macro_name(row[0])] = row

    text = text.split("\\begin{document}", 1)[1]

    info = section_split(text)  # creates tree, split into section, subsection, subsubsection, etc.

    output = create_general_pages(info) + create_specific_pages(info, glossary)
    output = output.replace("<br /><br />", "<br />")

    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(output)

if __name__ == '__main__':
    main()

    compare_files.compare(OUTPUT_FILE.replace("/", "\\").replace(".mmd", ""))
