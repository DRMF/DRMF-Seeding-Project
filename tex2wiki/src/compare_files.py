import os


def compare(output_file):
    commands = [
        "TYPE %s.mmd | FIND /V \"\" > %s.frmt" % (output_file, output_file),
        "TYPE %s.mmd.bak | FIND /V \"\" > %s.bak.frmt" % (output_file, output_file),
        "fc /N %s.frmt %s.bak.frmt > tex2wiki\\data\\output.txt" % (output_file, output_file)
    ]

    for command in commands:
        os.system(command)
