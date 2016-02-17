# DRMF-Seeding-Project

This project is meant to convert different designated source formats to semantic LaTeX for the
DRMF project. One major aspect of this conversion is the inclusion, insertion, and replacement 
of LaTeX semantic macros.  

## MediaWiki Wikitext Generation

Currently empty. Needs to be uploaded.

## Macro-Replacement (KLS Seeding Project)

This Python code (mostly developed by Cherry Zou) performs macro replacements for the KLS Seeding Project.
Parts of this code were developed by Alex Danoff and Azeem Mohammed.

## Alex Danoff Seeding Source Code

To achieve the desired result, one should execute the progams in the following order (using the output of the previous program as input for the next one):

1. remove_excess.py
2. replace_special.py
3. prepare_annotations.py

## eCF Seeding Project

## DLMF Seeding Project

## BMP Seeding Project

## KLSadd Insertion Project
linetest.py and updateChapters (mostly) written by Rahul Shah (ILIKEFUUD)

Edits the DRMF chapter files to include the relevant KLS addendum additions. Additions are (currently) only being added right before the "References" paragraphs in each section. The linetest.py file is the first working model of the code, but it is very messy and esoteric. Comments have been made to aid interpretation. The new project file, updateChapters.py is a more readable version, but not quite up to date. 

Left to do in updateChapters.py:
import over the necessary files to make the pdf work, change all instances of "section" to "paragraph" and add "\large\bf" to make font large and bold like the other chapter headings. Also necessary to add initials of programmer wherever the new additions were added (ex. "%RS added, %RS end") 

Also: rewrite code for "smarter" edits (ex. add new limit relations straight to the 
