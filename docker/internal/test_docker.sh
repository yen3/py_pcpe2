#!/usr/bin/env bash

git pull
git submodule update

pip3 install -r requirements.txt
python3 setup.py develop
nosetests --detailed-errors --with-doctest -v
