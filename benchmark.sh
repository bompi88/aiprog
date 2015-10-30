#!/usr/bin/env bash
./src/clibs/compile.sh
time python -m src.algorithms.adversial_search.expectimax_c
