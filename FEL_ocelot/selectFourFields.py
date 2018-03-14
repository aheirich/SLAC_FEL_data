#
# selectFourFields.py
#
# read an output file produced by extract.py
# pull out four desired fields to combine with the Anthony script data
#

import sys


fields = [ ' QUAD_LI26_201_BCTRL', ' charge', ' current', ' timestamps', ' GDET_FEE1_241_ENRCHSTBR' ]
index = []

for line in sys.stdin:
  words = line.strip().split(',')
  
  if line.startswith('quads:'):
    continue
  
  if line.startswith('keys:'):
    string = ''
    for i in range(len(words)):
      if words[i] in fields:
        index.append(i)
        string = string + words[i] + ','
    print string
    continue

  if len(index) > 0:
    string = ''
    for i in range(len(words)):
      if i in index:
        string = string + words[i] + ','
    print string
