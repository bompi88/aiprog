#!/usr/bin/env bash
mkdir -p tmp
mkdir -p pdfs

echo "Making module 5"
pdflatex -output-directory=tmp module_5 > /dev/null
echo "Moving module 5"
mv tmp/module_5.pdf pdfs/

echo "Making module 6"
pdflatex -output-directory=tmp module_6 > /dev/null
echo "Moving module 6"
mv tmp/module_6.pdf pdfs/

echo "Making Project 3"
pdflatex -output-directory=tmp project > /dev/null

echo "Moving Project 3"
mv tmp/project.pdf pdfs/project3.pdf
