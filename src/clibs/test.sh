#!/usr/bin/env bash
# cc -g -O0 expectimax.c
# valgrind --leak-check=yes ./a.out
# rm a.out

/usr/local/bin/gcc-5 -O2 -g -Wall -std=c99 -Wno-padded -Wno-conversion -pedantic -o expectimax expectimax.c
./expectimax
valgrind --tool=callgrind ./expectimax
rm expectimax
