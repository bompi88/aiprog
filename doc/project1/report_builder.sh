#!/usr/bin/env bash
mkdir -p tmp
mkdir -p pdfs

echo "Making module 1"
pdflatex -output-directory=tmp module_1 > /dev/null
echo "Moving module 1"
mv tmp/module_1.pdf pdfs/

echo "Making module 2"
pdflatex -output-directory=tmp module_2 > /dev/null
echo "Moving module 2"
mv tmp/module_2.pdf pdfs/

echo "Making module 3"
pdflatex -output-directory=tmp module_3 > /dev/null
echo "Moving module 3"
mv tmp/module_3.pdf pdfs/

echo "Making Project 1"
pdflatex -output-directory=tmp project > /dev/null

echo "Moving Project 1"
mv tmp/project.pdf pdfs/project1.pdf
