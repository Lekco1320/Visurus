#!/bin/bash

source ../src/venv/bin/activate
pip3 install --upgrade nuitka

python3 -m nuitka \
--standalone \
--onefile \
--enable-plugin=tk-inter \
--nofollow-import-to=requests,numpy \
--remove-output \
--output-dir=. \
--output-filename="Visurus" \
--linux-onefile-icon=./logo.png \
../src/main.py

mv ./Visurus ../src
