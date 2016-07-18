#!/bin/sh
set -e
set -o pipefail

cd AlexDanoff
echo ls
python -m unittest discover

