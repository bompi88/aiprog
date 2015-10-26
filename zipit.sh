#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied, usage: ./zipit.sh (project1 | project2 | project3 | project4)"
else

    cd "doc/$1"

    ./report_builder.sh

    cd -

    mkdir -p delivery/doc

    # all docs
    cp "doc/$1/pdfs/$1.pdf" "delivery/doc/$1.pdf"

    find src -name '*.py' -o -name '*.c' -o -name '*.h' -o -name '*.sh' | cpio -pdm delivery
    find res -name '*.py' -o -name '*.txt' -o -name '*.png' | cpio -pdm delivery
    find tests -name '*.py' -o -name '*.c' -o -name '*.h' | cpio -pdm delivery
    cp run.sh delivery/run.sh
    cp tests.sh delivery/tests.sh

    zip -r delivery.zip delivery

    rm -r delivery
fi