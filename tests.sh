#!/bin/sh

cd AlexDanoff
echo ls
python -m unittest discover
rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

