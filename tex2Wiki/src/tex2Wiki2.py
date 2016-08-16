__author__ = "Joon Bang"
__status__ = "Prototype"

METADATA_TYPES = {"substitution": "Substitution(s)", "constraint": "Constraint(s)"}


class LatexEquation(object):
    def __init__(self, label, equation, metadata):
        self.label = label
        self.equation = equation
        self.metadata = metadata

    def __str__(self):
        return self.label + "\n" + self.equation + "\n" + str(self.metadata)


def generate_html(tag_name, options, text, spacing=True):
    # (str, str, str(, bool)) -> str
    """Generates an html tag, with optional html parameters."""
    result = "<" + tag_name
    if options != "":
        result += " " + options

    result += ">"

    if tag_name == "math":
        result += "{\\displaystyle"

    result += "\n" + text + "\n"

    if tag_name == "math":
        result += "}"

    result += "</" + tag_name + ">\n"

    if not spacing:
        return result.replace("\n", " ")[:-1] + "\n"

    return result


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
    for ch in string:
        if ch == "$" and count % 2 == 0:
            result += "<math>{\\displaystyle "
            count += 1
        elif ch == "$":
            result += "}</math>"
            count += 1
        else:
            result += ch

    return result


def translate(data):
    result = list()
    for section_data in data:
        equations = section_data[1][:-1]
        for i, equation in enumerate(equations):
            # formula stuff
            try:
                formula = get_data_str(equation, latex="\\formula")
                formula = formula.split("Formula:", 1)[1]
            except IndexError:  # there is no formula.
                break

            # get metadata
            raw_metadata = list()

            equation = equation.split("\n")[1:]

            j = 0
            while j < len(equation):
                if "%" in equation[j]:
                    raw_metadata.append(equation.pop(j))
                else:
                    j += 1

            raw_metadata = ''.join([line[1:].strip() for line in raw_metadata])

            metadata = dict()
            for data_type in METADATA_TYPES:
                metadata[data_type] = convert_dollar_signs(get_data_str(raw_metadata, latex="\\"+data_type)).strip()

            equations[i] = LatexEquation(formula, ' '.join(equation), metadata)

        result.append([section_data[0], equations])

    return result


def create_general_pages(data):
    ret = ""

    for section_data in data:
        section_name = section_data[0]
        result = "drmf_bof\n'''" + section_name + "'''\n{{DISPLAYTITLE:" + section_name + "}}\n"

        # TODO: headers code (recycle from main_page code?)

        result += "\n== " + section_name + " ==\n\n"

        text = ""
        for equation in section_data[1]:
            # equation is of type LatexEquation
            text += generate_html("math", "id=\"" + equation.label + "\"", equation.equation)

            for data_type, info in equation.metadata.iteritems():
                if info != "":
                    text += generate_html("div", "align=\"right\"", METADATA_TYPES[data_type] + ": " + info,
                                          spacing=False)[:-1] + "<br />\n"

        result += text + "drmf_eof\n"

        ret += result

    return ret


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


def main():
    with open("tex2Wiki/data/01outb.tex") as input_file:
        text = input_file.read()

    text = text.split("\\begin{document}", 1)[1]
    text = text.split("\\section")

    title = get_data_str(text[0])
    print title

    data = list()
    for section in text[1:]:
        section_name = get_data_str(section).replace("$", "''")
        equations = section.split("\\end{equation}")
        for i, equation in enumerate(equations[:-1]):
            equations[i] = equation.split("\\begin{equation}", 1)[1].strip()

        data.append([section_name, equations])

    data = translate(data)
    print create_general_pages(data)

if __name__ == '__main__':
    main()
