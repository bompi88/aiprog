#!/usr/bin/env bash
cd doc/project1

./report_builder.sh

cd -

mkdir -p delivery/doc

# all docs
cp doc/project1/pdfs/project_1.pdf delivery/doc/project_1.pdf

find src -name '*.py' | cpio -pdm delivery
find res -name '*.py' -o -name '*.txt' -o -name '*.png' | cpio -pdm delivery
find tests -name '*.py' | cpio -pdm delivery
cp run.sh delivery/run.sh
cp tests.sh delivery/tests.sh

zip -r delivery.zip delivery

rm -r delivery
