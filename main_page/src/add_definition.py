__author__ = "Joon Bang"
__status__ = "Development"


def main():
    macro_name = raw_input("Macro name: ")
    definition = raw_input("LaTeX definition: ")

    result = "drmf_bof\n" + \
             "'''Definition:" + macro_name + "'''\n" + \
             "The LaTeX DLMF and DRMF macro '''\\" + macro_name + "''' represents the " + macro_name + ".\n\n" + \
             "These are defined by \n" + \
             "<math>{\\displaystyle\n" + definition + "\n}</math>\n<br />\n\ndrmf_eof\n"

    with open("main_page/main_page.mmd", "a") as main_page:
        main_page.write("\n" + result)

    print "\n" + result


if __name__ == '__main__':
    main()
