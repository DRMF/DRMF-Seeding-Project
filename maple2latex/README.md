# Maple CFSF Seeding Project
This project uses Python to convert the continued fractions for special functions library, written in Maple, into LaTeX. 

## Prerequisites
This program requires Python 2.6+ to run.

## Usage
To run the program, ensure that you are in the directory where maple2latex is located. Then, run the command `python maple2latex/src/main.py`.

Currently, the program translates only the CFSF library of functions. In the future, support will be added for 
translating individual .mpl files.

## Code Explanation
There are three files, `main.py`, `maple_tokenize.py`, and `translator.py`. The bulk of the code is located in `translator.py.`

The program works by parsing through "tokens," which are created by running the `tokenize` function on a string. 
It then goes through the tokens, joining them when necessary. It initially joins terms grouped in parentheses, starting from 
the innermost set of parentheses and working its way outwards. It has separate functions handling translation of mathematical 
functions, and basic operations (addition, multiplication, division, etc.). 
