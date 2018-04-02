#!/bin/bash
rm -f duplicates.log duplicate_timestamps.txt
while read duplicate ; do
  echo === for this duplicate control setting >> duplicates.log
  echo ${duplicate} >> duplicates.log
  grep -B 1 "${duplicate}" fel_input.py | grep "^#" | sort > duplicate_timestamps.txt
  wc -l duplicate_timestamps.txt >> duplicates.log
  while read duplicate_timestamp ; do
    echo "=== there should be exactly one output below :" >> duplicates.log
    grep -A 1 "${duplicate_timestamp}" FEL_OUTPUT.py | grep -v "^#" | sort | uniq > duplicate_outputs.txt
    cat duplicate_outputs.txt >> duplicates.log
    wc -l duplicate_outputs.txt >> duplicates.log
  done <duplicate_timestamps.txt
done <duplicates.txt
