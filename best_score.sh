#!/bin/bash
ID=$1
F=$2
grep -v "^#" $F | grep "^$ID" | sort -gk 11 | head -n 1 
