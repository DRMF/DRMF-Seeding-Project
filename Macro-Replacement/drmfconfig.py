import os
import sys
from snippets import *
from function import Function

class ConfigFile(object):
    """Represents a configuration file (containing regular expressions) used for seeding the DRMF"""

    #creates a new config file object from the file with name file_name
    def __init__(self, file_name, verbose=False):

        self._config_file = open(file_name, "r")
        self._file_name = file_name

        self._file_size = os.stat(file_name).st_size

        self._all_funcs = self._get_all_funcs(verbose)

    #read in config file and return all_funcs list
    def _get_all_funcs(self, verbose):

        offset = 0
        all_funcs = []
        self._config_file.seek(offset)

        #read in whole file
        while offset < self._file_size:

            chunk = ""
            in_line = ""

            #read in entire macro
            while not in_line.endswith("~?~"):

                in_line = self._config_file.readline().strip()
                offset += len(in_line)

                #skip line if it's empty or a comment
                if in_line == '' or in_line.startswith("%"):
                    in_line = ""
                    continue

                chunk += in_line
                offset += 2

            #  print(chunk + '\n')
            chunk = chunk[:-3]
            try:
                macro, abbr, regexes, replacements, description = chunk.split("`")
            except ValueError as ve:
                print("ValueError: {0}".format(ve))
                print(chunk)
                sys.exit(-1) 
            regexes = regexes.split("~-~")
            replacements = replacements.split("~-~")

            #create each regular expression and replacement from the strings in the file
            try:
                regexes = [eval(regex) for regex in regexes]
                replacements = [eval(replacement) for replacement in replacements]
            except SyntaxError as se:
                print("ERROR IN CONFIG FILE: {0}\n\tSYNTAX ERROR ON REGEX FOR {1}:".format(self._file_name, macro))
                print(se.text)
                sys.exit(-1)

            all_funcs.append(Function(macro, abbr, regexes, replacements, description, verbose=verbose))

        return all_funcs

    @property
    def all_funcs(self):
        return self._all_funcs
