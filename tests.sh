#!/usr/bin/env bash
echo "Pylint source files"
pylint src/ --rcfile=.pylintrc
echo "Pylint tests"
pylint tests/ --rcfile=.pylintrc

echo ""
echo "Unittests"
python3 -m unittest discover
