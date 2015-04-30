#!/usr/bin/env python
"""This module contains the code for the 'search' functionality of the DRMF seeding program."""

from collections import defaultdict
from replace import replacemid

def run(inputfile, outputfile, all_funcs):
    """Reads in the content from inputfile, counts the occurences of each macro on each line, and writes the result in a log format to outputfile."""

    identifiers_info = {}

    #create dictionary that maps identifiers to function names
    for func in all_funcs:
        identifiers_info[func.abbr] = (func.macro, func.description)
        
    line_lengths = [0]

    content = ""

    #read in input file and count line lengths
    with open(inputfile, "r") as in_file:

        total_length = 0

        for line in in_file.readlines():

            total_length += len(line)
            line_lengths.append(total_length)
	
            content += line

    frequencies = [[] for i in range(len(line_lengths))]

    content = replacemid(content)
   
    seen = set()

    #go through each function and add an entry to the correct frequency list for every match found
    for func in all_funcs:

        occurences = defaultdict(int) 

        #go through each starting point and find out what line it's on
        for start_byte in func.get_all_starts(content):

            seen.add(func.abbr)

            line_num = find_line(start_byte, line_lengths)
            occurences[line_num] += 1

        #go through each line with the current function on it and add an entry to the frequency list for that line
        for line_num in occurences:
            
            new_entry = (occurences[line_num], func.abbr)
            frequencies[line_num].append(new_entry)

    write_results(outputfile, frequencies, identifiers_info, seen)

def find_line(byte, line_lengths):
    """Determines which line the character byte bytes from the start of the file occurs on using a binary search."""
    
    return _find_line_helper(byte, line_lengths, 0, len(line_lengths))

#uses recursive binary-search-esque algorithm to find what line the given byte is on
def _find_line_helper(byte, line_lengths, start, end):

    mid = (start + end) // 2

    next_start = start
    next_end = end

    #target byte is less than mid
    if byte < line_lengths[mid]:

        left = mid - 1

        #target byte between left and mid
        if line_lengths[left] < byte:
            return mid

        next_end = left

    #target byte is between mid and right
    if line_lengths[mid] <= byte:

        right = mid + 1

        #target byte between mid and right
        if byte < line_lengths[right]:
            return right

        next_start = right

    return _find_line_helper(byte, line_lengths, next_start, next_end)

def write_results(outputfile, frequencies, identifiers_info, seen):
    """Writes the completed frequencies list to output file in the appropriate format."""
    
    #write the frequencies to the file
    with open(outputfile, "w") as out_file:

        #go through every line of the input file
        for line_num in range(len(frequencies)):

            to_write = "{0}:".format(line_num) 
            to_write = "{0:<6}".format(to_write)

            #only write if there are macros on the current line
            if len(frequencies[line_num]) == 0:
                continue

            #for every function on the line, output the number of times it occured on that line and its abbreviation
            for occurences, abbr in frequencies[line_num]: 

                to_write += ":{0} {1}".format(abbr, occurences)

            to_write = to_write[:] + ":\n"
            out_file.write(to_write)

        out_file.write("\n\n" + create_usage_table(identifiers_info, seen))

def create_usage_table(identifiers_info, seen):
    """Creates a table displaying the used identifiers and the macros they represent"""
    
    format = "^70"
    layout = "||| {0:^16} ||| {1:{3}} ||| {2:{3}} |||\n" 

    table_str = layout.format("Identifier", "Macro", "Description", format)
 
    underline_length = int(format[1:]) * 3
    underline_string = "-" * underline_length

    table_str += underline_string + "\n"

    layout = layout.replace("^", "<")
    format = "<70"

    #go through each identifier that we have seen and add its entry to the table
    for identifier in seen:

        macro = identifiers_info[identifier][0]
        description = identifiers_info[identifier][1]

        table_str += layout.format(identifier, macro, description, format)

    return table_str

def main():
    lengths = [0, 5, 10, 15, 20, 25]
    print(lengths)
    for i in range(25):
        print("{0}: {1} ".format(i, find_line(i, lengths)))

if __name__=="__main__":
    main()
