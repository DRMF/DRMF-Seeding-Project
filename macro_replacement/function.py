import re

class Function(object):
    """This class represents a mathematical function or polynomial. It provides methods to search for the function and replace it using a given replace function"""

    #create the function object with the given name, abbreviation, regex patterns, and replacement function
    def __init__(self, macro, abbr, regexes, replacements, description, verbose=False):
        
        #ensure correct number of regexes and replacements have been provided
        if len(regexes) != len(replacements):
            raise ValueError(name + " - must provide the same number of replacements as regexes")

        self._macro = macro
        self._abbr = abbr
        self._regexes = regexes
        self._replace = replacements
        self._description = description
        self._verbose = verbose

#        self._name = macro[1:macro.index("{")]

    #finds the pattern in content using regexes
    def make_subs(self, content):

        total = 0
        counter = 0

        #use each regex/replacement pair to make substitutions
        for regex, replacement in zip(self._regexes, self._replace):
            pattern = None

            try:
                pattern = re.compile(regex)
            except Exception as e:
                print("\t\t\t\tERROR WHEN CREATING REGEX - {0} - {1} - {2}".format(regex, self._macro, e))

            all_matches = pattern.findall(content)
            total += len(all_matches) 
            content = re.sub(pattern, self._move_and, content)
            
            try:
                content = re.sub(pattern, replacement, content)
            except Exception  as e:
                print("ERROR IN MAKING SUBSTITUTIONS FOR FUNCTION {0}: REGEX: {1} REPLACEMENT: {2} - {3}".format(self._macro, regex, replacement, e))
            counter += 1

            #only print out info if verbose is specified
            if self._verbose:
                print("MAKING SUBS FOR {0} WITH REGEX #{1}".format(self._macro, counter))
                for match in all_matches:
                    print("\t{0}".format(match))

                print("\tTOTAL SUBS FOR {0} ({1} REGEXES): {2}".format(self._macro, len(self._regexes), total))

        return content

    #moves and ampersands from in the macro to the beginning
    def _move_and(self, match):

        match = match.group(0)
        init_len = len(match)

        and_pat = re.compile(r'(?<!\\)&')

        if and_pat.findall(match):
            match = and_pat.sub('', match)
            match = "&" + match

        return match

    #getters for macro abbreviation and description
    @property
    def macro(self):
        return self._macro

    @property
    def description(self):
        return self._description

    @property
    def abbr(self):
        return self._abbr

    def get_all_starts(self, content):
        """Returns a list of the starting character index in content of every match for this function."""

        starts = []

        #use each pattern given in the config file
        for regex in self._regexes:
            pattern = None

            try:
                pattern = re.compile(regex)
            except Exception as e:
                print("\t\t\t\tERROR WHEN CREATING REGEX - {0} - {1} - {2}".format(regex, self._macro, e))

            #go through each match and add its starting location
            for match in pattern.finditer(content):
                
                #print more info if verbose
                if self._verbose:
                    print("{0} - {1} - {2} - {3}".format(self._name, regex, match.start(),  match.group()))

                starts.append(match.start())
                
            #returns a string that maintains the number of lines in the file but will not match further patterns
            def repl(match):
                return  "\n" * match.group().count("\n") 

            content = pattern.sub(repl, content)

        return starts

    #counts the number of times each pattern occurs in lines
    def count(self, lines):
        
        occurences = 0

        #use each regex to count occurences
        for regex in self._regexes:

            if regex is r'\(Q_(\w+)Q_(\w+)\)(?:\\left|\\Bigg|\\bigg|\\big|\\Big|\\bigl)?\((.*?);(.*?),(.*?);q(?:\\right|\\Bigg|\\bigg|\\big|\\Big|\\bigr)?\)':
                print('hi')
                occurences += 2
                continue
             
            regex = re.compile(regex)
            occurences += len(regex.findall(lines))
            lines = regex.sub(' ', lines)                            #replace matches with ' ' to avoid rematching


        return occurences
