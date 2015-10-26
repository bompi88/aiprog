#!/usr/bin/env bash
cc -Weverything -Wno-padded -Wno-conversion -pedantic -shared -o "`dirname $0`/expectimax_lib.so" "`dirname $0`/expectimax.c"
echo "Compiled expectimax.c"
