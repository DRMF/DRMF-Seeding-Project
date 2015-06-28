# DRMF Macro Replacement Project

This project uses regular expressions and string methods to insert DLMF and DRMF macros into unprocesssed TeX based on the regular expressions specified in `function_regex`.

## Usage

The program should be run as follows:
```
python drmfdriver.py inputfile outputfile
```
Where:
* `inputfile` is a file containing the TeX source you wish to process
* `outputfile` is the file to write the processed TeX to

Flags:
* `-c` or `--config` allows you to specify a configuration file *[default=function_regex]*
* `-v` or `--verbose` will print out information about replacements as they occur
* `-s` or `--search` will write a log of replacements that should be made in the input file to the output file
* `-r` or `--replace` will make replacements from input file write them to the output file *[default]*

## Files

The project consists of several program files:
* `cosSubstitution.py` - resolves disparities with cosine formatting
* `drmfconfig.py`      - used to configure initial settings of program
* `drmfdriver.py`      - driver file
* `function.py`        - creates function objects and provides methods to search and replace functions
* `identifiers.py`     - inserts identifiers of functions to be replaced
* `monics.py`          - makes replacements for monic functions
* `normalized.py`      - makes replacements for normalized functions
* `parenthese.py`      - contains methods called by other files for convenience
* `replace.py`         - makes main body of function replacements
* `replace_special.py` - modifiers certain special symbols such as \pi and i
* `search.py`          - searches for functions to be replaced
* `snippets.py`        - contains snippets of code for use in other programs
* `utilities.py`       - contains methods called by other files for convenience

## Regular Expressions

In order to add new macros/replacements to the functionality of the program, one must edit the `function_regex` file. Entries in the file are in the following form:
```
%% comment
macroformat`macroidentifier`
regex_1~-~regex_2~-~...~-~regex_n`
replacement_1~-~replacement_2~-~...~-~replacement_n`
fullname~?~
```
Where:
* `macroformat` is a template for what the macro should look like in the output file (i.e. pochhammer{a}{n})
* `macroidentifier` is a 1-3 character "code" to help identify occurences of the macro
* `regex_1 - regex_n` are the Python regular expressions that will be used to identify TeX that should be replaced with the macro (a full reference for regular expressions in Python can be found [here](https://docs.python.org/3/library/re.html#module-re)).
* `replacement_1 - replacement_n` are the replacements for each corresponding regular expression. Backreferences are supported.
* `fullname` is a formal name/short description for the function
