import os

inp = raw_input("Update Main Page? (y or n)")
if inp != "n":
    print("List")
    os.system("python list.py")
    print("Symbols List")
    os.system("python symbolsList2.py")
    print("Headers")
    os.system("python headers.py")
    print("List Ways")
    os.system("python modMain.py")

print("Done")
