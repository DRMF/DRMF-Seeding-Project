# DRMF Macro Replacement Project

This project inserts DLMF and DRMF macros into unprocesssed TeX based on the regular expressions specified in `function_regex`.

## Usage

The program should be run as follows:
```
python drmfdriver.py inputfile outputfile
```
Where:
* `inputfile` is a file containing the TeX source you wish to process
* `outputfile` is the file to write the processed TeX to

Flags:
* `-c` or `--config` allows you to specify a configuration file *[default=`function_regex`]*
* `-v` or `--verbose` will print out information about replacements as they occur
* `-s` or `--search` will write a log of replacements that should be made in the input file to the output file
* `-r` or `--replace` will make replacements from input file write them to the output file *[default]*
