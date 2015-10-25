#!/usr/bin/env bash
cc -Weverything -Wno-conversion -pedantic -shared -o expectimax_lib.so expectimax.c
