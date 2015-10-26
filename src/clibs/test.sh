#!/usr/bin/env bash
cc -g -O0 expectimax.c
valgrind --leak-check=yes ./a.out
rm a.out