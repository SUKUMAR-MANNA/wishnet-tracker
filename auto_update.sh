#!/bin/bash

cd ~/wishnet-cloud

python3 test.py

git add .
git commit -m "auto update"
git push