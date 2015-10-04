#!/usr/bin/env bash
mkdir -p tmp
echo "Making module 1"
pdflatex -output-directory=tmp module_1 > /dev/null
echo "Moving module 1"
mv tmp/module_1.pdf pdfs/

echo "Making module 2(not yet..)"

echo "Making Project 1"
pdflatex -output-directory=tmp project > /dev/null

echo "Moving Project 1"
mv tmp/project.pdf pdfs/project_1.pdf
