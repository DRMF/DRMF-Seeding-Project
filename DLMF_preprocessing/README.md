# DRMF-Seeding-Project

## Alex Danoff Seeding Source Code

This code preprocesses code from the DLMF to get it ready to be run through tex2wiki.

To achieve the desired result, one should execute the progams in the following order (using the output of the previous program as input for the next one):

1. remove_excess.py
2. replace_special.py
3. prepare_annotations.py
