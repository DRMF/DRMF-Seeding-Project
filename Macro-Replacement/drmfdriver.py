#Driver file for the DRMF seeding program

from optparse import OptionParser, OptionValueError
import replace
import search
from drmfconfig import ConfigFile

#parse command line args and either replace or generate replacement file
def main():
    
    parser = OptionParser(usage="usage: %prog [options] inputfile outputfile")
    
    #validates mode, prevents both -r and -s
    def validate(option, opt_string, value, parser):

        to_raise = OptionValueError("cannot specify both search and replace")
        if opt_string == "--replace" or opt_string == "-r":

            if parser.values.replace: 
                raise to_raise 
            setattr(parser.values, "replace", True)

        else:

            if parser.values.search: 
                raise to_raise 
            setattr(parser.values, "search", True)

    parser.add_option("-r", "--replace", default=False, action="callback", dest="replace", callback=validate, help="make replacements from input file write them to the output file [default]" )
    parser.add_option("-s", "--search", default=False, action="callback", dest="search", callback=validate, help="write a log of replacemnts that should be made in the input file to the output file (including line numbers)")

    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="print out information about replacements as they occur")
    
    parser.add_option("-c", "--config", action="store", default="function_regex", dest="config_file_name", help="the name of the configuration file to use")

    options, args = parser.parse_args()

    #ensure both input file and output file are present
    if len(args) != 2:
        raise TypeError("must specify both input file and output file")

    in_file = args[0]
    out_file = args[1]

    #no action specified, default to replace
    if not (options.replace or options.search):
        options.replace = True

    #user specified replace option
    if options.replace:
        to_run = replace

    #user specified search option
    else:
        to_run = search

    func_list = ConfigFile(options.config_file_name, verbose=options.verbose).all_funcs    

    to_run.run(in_file, out_file, func_list)

#call main function when this file is run directly
if __name__ == "__main__":
    main() 

