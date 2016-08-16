__author__ = "Joon Bang"
__status__ = "Prototype"


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
    result += ">\n" + text + "\n</" + tag_name + ">\n"

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
    for section_data in data:
        print section_data[0]
        equations = section_data[1]
        for i, equation in enumerate(equations):
            # formula stuff
            try:
                formula = get_data_str(equation, latex="\\formula")
                formula = formula.split("Formula:", 1)[1]
            except IndexError:  # there is no formula.
                break

            # get metadata
            raw_metadata = list()
            metadata_types = {"substitution": "Substitution(s)", "constraint": "Constraint(s)"}

            equation = equation.split("\n")[1:]

            j = 0
            while j < len(equation):
                if "%" in equation[j]:
                    raw_metadata.append(equation.pop(j))
                else:
                    j += 1

            raw_metadata = ''.join([line[1:].strip() for line in raw_metadata])

            metadata = dict()
            for data_type in metadata_types:
                metadata[data_type] = convert_dollar_signs(get_data_str(raw_metadata, latex="\\"+data_type))

            equations[i] = LatexEquation(formula, ''.join(equation), metadata)

        for equation in equations:
            print equation


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

    translate(data)

if __name__ == '__main__':
    main()
