#!/usr/bin/env bash
mkdir -p tmp
mkdir -p pdfs

echo "Making module 4"
pdflatex -output-directory=tmp module_4 > /dev/null
echo "Moving module 4"
mv tmp/module_4.pdf pdfs/

echo "Making Project 1"
pdflatex -output-directory=tmp project > /dev/null

echo "Moving Project 1"
mv tmp/project.pdf pdfs/project2.pdf
