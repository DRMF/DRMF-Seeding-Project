__author__ = "Azeem Mohammed"
__status__ = "Development"

import os


# TODO: Actually make the if statements do what they're supposed to.

if raw_input("Update Main Page? (y or n) ") != "n":
    print "List"
    os.system("python src/list.py")
    print "Symbols List"
    os.system("python src/symbols_list.py")
    print "Headers"
    os.system("python src/headers.py")
    print "List Ways"
    os.system("python src/mod_main.py")

print "Done"
