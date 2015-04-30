# DRMF Macro Replacement Project

This project inserts DLMF and DRMF macros into unprocesssed TeX based on the regular expressions specified in `function_regex`.

##Usage

The program should be run as follows:
```
python drmfdriver.py inputfile outputfile
```
Where:
* `inputfile` is a file containing the TeX source you wish to process
* `outputfile` is the file to write the processed TeX to
