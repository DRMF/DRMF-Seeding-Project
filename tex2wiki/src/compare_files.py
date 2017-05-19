import os


def compare(output_file, number=0):
    commands = [
        "TYPE %s.mmd | FIND /V \"\" > %s.frmt" % (output_file, output_file),
        "TYPE %s.mmd.bak | FIND /V \"\" > %s.bak.frmt" % (output_file, output_file),
        "fc /N %s.frmt %s.bak.frmt > tex2wiki\\data\\output%s.txt" % (output_file, output_file, str(number))
    ]

    for command in commands:
        os.system(command)
