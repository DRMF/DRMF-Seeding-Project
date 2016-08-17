__author__ = "Joon Bang"
__status__ = "Prototype"

INPUT_FILE = "tex2Wiki/data/01outb.tex"
OUTPUT_FILE = "tex2Wiki/data/01outb.mmd"
GLOSSARY_LOCATION = "tex2Wiki/src/new.Glossary.csv"
METADATA_TYPES = {"substitution": "Substitution(s)", "constraint": "Constraint(s)"}

import csv


class LatexEquation(object):
    def __init__(self, label, equation, metadata):
        self.label = label
        self.equation = equation
        self.metadata = metadata


def generate_html(tag_name, text, options=dict(), spacing=2):
    # (str, str(, dict, bool)) -> str
    """
    Generates an html tag, with optional html parameters.
    When spacing = 0, there should be no spacing.
    When spacing = 1, the tag, text, and end tag are padded with spaces.
    When spacing = 2, the tag, text, and end tag are padded with newlines.
    """
    option_text = [key + "=\"" + value + "\"" for key, value in options.iteritems()]
    result = "<" + tag_name + " " * (option_text != []) + ", ".join(option_text) + ">"

    if spacing == 2:
        result += "\n" + text + "\n</" + tag_name + ">\n"
    elif spacing == 1:
        result += " " + text + " </" + tag_name + ">"
    else:
        result += text + "</" + tag_name + ">"

    return result


def generate_math_html(text, options=dict(), spacing=True):
    """
    Special case of generate_html, where the tag is "math".
    """
    option_text = [key + "=\"" + value + "\"" for key, value in options.iteritems()]
    result = "<math" + " " * (option_text != []) + ", ".join(option_text) + ">"

    if spacing:
        result += "{\\displaystyle\n" + text + "\n}</math>\n"
    else:
        result += "{\\displaystyle " + text + "}</math>\n"

    return result


def generate_link(left, right=""):
    """Generates a link thingie."""

    if right == "":
        return "[[" + left + "|" + left + "]]"

    return "[[" + left + "|" + right + "]]"


def multi_split(s, seps):
    """Copy pasted from internet!"""
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res


def convert_dollar_signs(string):
    count = 0
    result = ""
    for i, ch in enumerate(string):
        if ch == "$" and count % 2 == 0:
            result += "<math>{\\displaystyle "
            count += 1
        elif ch == "$":
            result += "}</math>"
            count += 1
        else:
            result += ch

    return result


def format_formula(formula):
    formula = multi_split(formula.split("Formula:", 1)[1], [".", ":"])

    for j in [-1, -2, -3]:
        formula[j] = formula[j].zfill(2)

    if len(formula) == 3:
        formula = formula[0] + "." + formula[1] + ":" + formula[2]
    else:
        formula = ":".join(formula[:-3]) + ":" + formula[-3] + "." + formula[-2] + ":" + formula[-1]

    return formula


def format_metadata(string):
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
    result = list()
    for section_data in data:
        equations = section_data[1][:-1]
        for i, equation in enumerate(equations):
            # formula stuff
            try:
                formula = format_formula(get_data_str(equation, latex="\\formula"))
            except IndexError:  # there is no formula.
                break

            equation = equation.split("\n")[1:]

            # get metadata
            percent_list = list()
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

            # print metadata

            equations[i] = LatexEquation(formula, '\n'.join(equation), metadata)

        result.append([section_data[0], equations])

    return result


def find_end(text, left_delimiter, right_delimiter, start=0):
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
    if latex + "{" not in text:
        return ""

    start = text.find(latex + "{")
    return text[start + len(latex + "{"):find_end(text, "{", "}", start)]


def generate_nav_bar(main_title, hash_code, sections, i, middle=""):
    # TODO: Rewrite this function.

    sections = ["Orthogonal Polynomials"] + sections + ["Orthogonal Polynomials"]

    center_text = (main_title + "#" + hash_code).replace(" ", "_")

    sections = [s.replace("''", "") for s in sections]

    if middle == "":
        middle = sections[i + 1]

    nav_section = generate_html("div", "<< " + generate_link(sections[i]), options={"id": "alignleft"},
                                spacing=1) + "\n" + \
                  generate_html("div", generate_link(center_text, middle), options={"id": "aligncenter"},
                                spacing=1) + "\n" + \
                  generate_html("div", generate_link(sections[i + 2]) + " >>", options={"id": "alignright"},
                                spacing=1)

    header = generate_html("div", nav_section, options={"id": "drmf_head"})
    footer = generate_html("div", nav_section, options={"id": "drmf_foot"})

    return header, footer


def get_macro_name(macro):
    # (str) -> str
    """Obtains the macro name."""
    macro_name = ""
    for ch in macro:
        if ch.isalpha() or ch == "\\":
            macro_name += ch
        elif ch in ["@", "{", "["]:
            break

    return macro_name


def find_all(pattern, string):
    # (str, str) -> generator
    """Finds all instances of pattern in string."""

    i = string.find(pattern)
    while i != -1:
        yield i
        i = string.find(pattern, i + 1)


def get_symbols(text, glossary):
    # (str, dict) -> str
    """Generates span text based on symbols present in text."""
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


def create_general_pages(data, title):
    ret = ""

    section_names = [d[0] for d in data]  # list of section names

    for i, section_data in enumerate(data):
        section_name = section_data[0]
        result = "drmf_bof\n'''" + section_name.replace("''", "") + "'''\n{{DISPLAYTITLE:" + section_name + "}}\n"

        # header/footer code
        header, footer = generate_nav_bar("Orthogonal Polynomials", "Sections in " + title, section_names, i)

        result += header + "\n== " + section_name + " ==\n\n"

        text = ""
        for eq in section_data[1]:
            # equation is of type LatexEquation
            text += generate_math_html(eq.equation, options={"id": eq.label})

            metadata_exists = False
            for data_type in sorted(eq.metadata.keys()):
                if eq.metadata[data_type] != "":
                    text += generate_html("div", METADATA_TYPES[data_type] + ": " + eq.metadata[data_type],
                                          options={"align": "right"}, spacing=False) + "<br />\n"
                    metadata_exists = True

            if not metadata_exists:
                text = text[:-1] + "<br />\n"

        result += text + footer + "\n" + "drmf_eof\n"

        ret += result

    return ret


def create_specific_pages(data):
    pages = list()

    formulae = list()
    for section_data in data:
        for equations in section_data[1:]:
            for eq in equations:
                formulae.append("Formula:" + eq.label)
            formulae.append(section_data[0])

    print formulae

    glossary = dict()
    with open(GLOSSARY_LOCATION, "rb") as csv_file:
        glossary_file = csv.reader(csv_file, delimiter=',', quotechar='\"')
        for row in glossary_file:
            glossary[get_macro_name(row[0])] = row

    i = 0
    for j, section_data in enumerate(data):
        section_name = section_data[0]
        for eq in section_data[1]:
            header, footer = generate_nav_bar(section_name, eq.label, formulae, i, middle="formula in " + section_name)

            result = "drmf_bof\n'''Formula:" + eq.label + "'''\n{{DISPLAYTITLE:Formula:" + eq.label + "}}\n" + header \
                     + "\n<br />"

            result += generate_html("div", generate_math_html(eq.equation)[:-1], options={"align": "center"},
                                    spacing=0) + "\n\n"

            for data_type, info in eq.metadata.iteritems():
                if info != "":
                    result += "== " + METADATA_TYPES[data_type] + " ==\n\n"
                    result += generate_html("div", info, options={"align": "left"}, spacing=0) + "<br />\n\n"

            result += "== Proof ==\n\nWe ask users to provide proof(s), reference(s) to proof(s), or further " \
                      "clarification on the proof(s) in this space.\n\n== Symbols List ==\n\n"
            result += get_symbols(result, glossary) + "\n<br />\n\n"

            result += "== Bibliography ==\n\n"
            result += "<span class=\"plainlinks\">[http://homepage.tudelft.nl/11r49/askey/contents.html " \
                      "Equation in Section 1." + str(j + 1) + "]</span> of [[Bibliography#KLS|'''KLS''']]."

            result += "\n\n== URL links ==\n\nWe ask users to provide relevant URL links in this space.\n\n"

            result += "<br />" + footer + "\ndrmf_eof"
            pages.append(result)

            i += 1

        i += 1

    return "\n".join(pages) + "\n"


def main():
    with open(INPUT_FILE) as input_file:
        text = input_file.read()

    text = text.split("\\begin{document}", 1)[1]
    text = text.split("\\section")

    title = get_data_str(text[0])

    data = list()
    for section in text[1:]:
        section_name = get_data_str(section).replace("$", "''")
        equations = section.split("\\end{equation}")
        for i, equation in enumerate(equations[:-1]):
            equations[i] = equation.split("\\begin{equation}", 1)[1].strip()

        data.append([section_name, equations])

    data = extract_data(data)
    output = create_general_pages(data, title) + create_specific_pages(data)

    with open(OUTPUT_FILE, "w") as output_file:
        output_file.write(output)

if __name__ == '__main__':
    main()
