import glob
import sys

sys.path.append('../../AlexDanoff/src')
from utilities import readin as readin
from utilities import writeout
from remove_excess import remove_excess as step1
from replace_special import remove_special as step2
from prepare_annotations import prepare_annotations as step3

sys.path.append('../../Azeem/src')
from tex2Wiki import readin as step4
from tex2Wiki import writeout as step5


# step1 = imp.load_source('remove_excess','../../AlexDanoff/src/remove_excess.py')

def main():
    if len(sys.argv) != 2:
        pattern = "../../data/[0-9]*ZE.tex"  # [A-Z][A-Z]
    else:
        pattern = sys.argv[1]
    for fname in glob.glob(pattern):
        print "Processing " + fname
        writeout(fname + "-processed.tex", step3(step2(step1(readin(fname)))))
        step4(fname + "-processed.tex")
        step5(fname + "-dump.xml")


if __name__ == "__main__":
    main()
