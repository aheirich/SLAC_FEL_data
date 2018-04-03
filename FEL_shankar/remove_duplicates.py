#!/usr/bin/python
#
# remove_duplicates.bash
#
# 

import sys


if len(sys.argv) != 3:
  print('usage:', sys.argv[0], ' removal_candidates_forward.log FEL_INPUT.py')
  sys.exit(1)

# first build the list of bad entries
maxDeviation = 1.0
badList = []
batch = []

candidateFile = open(sys.argv[1], 'r')

for line in candidateFile:
  words = line.strip().split(' ')
  
  if words[0] == '===':
    deviation = float(words[6])
    if deviation > maxDeviation:
      for words in batch:
        badList.append(words[1])
    batch = []
  else:
    batch.append(words)

candidateFile.close()

dataFile = open(sys.argv[2], 'r')
isGood = True

for line in dataFile:
  line = line.strip()
  words = line.split(' ')
  if words[0] == '#':
    savedLine = line
    if words[1] in badList:
      isGood = False    
    else:
      isGood = True
  elif words[0].startswith('['):
    if isGood:
      print savedLine
      print line
  else:
    print line


dataFile.close()

