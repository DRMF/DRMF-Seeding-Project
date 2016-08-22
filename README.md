# DRMF-Seeding-Project

[![Build Status](https://travis-ci.org/DRMF/DRMF-Seeding-Project.svg?branch=master)](https://travis-ci.org/DRMF/DRMF-Seeding-Project)
[![Coverage Status](https://coveralls.io/repos/github/DRMF/DRMF-Seeding-Project/badge.svg?branch=master)](https://coveralls.io/github/DRMF/DRMF-Seeding-Project?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b097e91550e147b2b02e345ffb1c5162/badge.svg)](https://www.quantifiedcode.com/app/project/b097e91550e147b2b02e345ffb1c5162)
[![Code Health](https://landscape.io/github/DRMF/DRMF-Seeding-Project/master/landscape.svg?style=flat)](https://landscape.io/github/DRMF/DRMF-Seeding-Project/master)

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

1. `remove_excess.py`
2. `replace_special.py`
3. `prepare_annotations.py`

## BMP Seeding Project

## Maple CFSF Seeding Project

This Python code (developed by Joon Bang) translates Maple files from Annie Cuyt's continued fractions package for special functions (CFSF) to LaTeX.

The project is located in the `maple2latex` folder.

## DLMF Seeding Project

## Mathematica eCF Seeding Project

This Python code (mostly developed by Kevin Chen) translates Mathematica files to LaTeX.

The project is currently awaiting approval to be merged into the main branch of the repository.

## KLSadd Insertion Project
`linetest.py` and `updateChapters.py` written by Rahul Shah and Edward Bian

Edits the DRMF chapter files to include the relevant KLS addendum additions. Additions are (currently) only being added right before the "References" paragraphs in each section. The `linetest.py` file is the first working model of the code, but it is very messy and esoteric. Comments have been made to aid interpretation. The new project file, `updateChapters.py` is a more readable version.

TODO in `updateChapters.py`:

FINISHED- implemented smart fix for "hypergeometric representation" paragraphs. Now the content in these paragraphs are appended directly from the KLS section into the chapter's hypergeometric representation paragraphs

Needs to be done:
-implement the same smart fix for "Limit relations" paragraphs. Current code for this implementation does not work and has spotty logic that does not encompass all variations of limit relations paragraphs (such as the one subsubsection in chapter 9)
