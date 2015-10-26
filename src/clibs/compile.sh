#!/usr/bin/env bash
/usr/local/bin/gcc-5 -O2 -Wall -std=c99 -Wno-padded -Wno-conversion -pedantic -shared -o "`dirname $0`/expectimax_lib.so" "`dirname $0`/expectimax.c"
echo "Compiled expectimax.c"
