#!/usr/bin/python
#
# randomInitializer.py
#

import sys, random

if len(sys.argv) >= 3:
  numHiddenLayers = int(sys.argv[1])
  numHiddenUnitsPerLayer = int(sys.argv[2])
else:
  print 'please provide numLayers and numHiddenUnitsPerLayer'
  print 'eg 2 2048'
  sys.exit(1)

if len(sys.argv) > 4:
  random.seed(int(sys.argv[3]))
else:
  random.seed(None)


def randomValue():
  maxRandom = 1000000000
  r = random.randint(0, maxRandom) - (maxRandom / 2)
  value = float(r) / (maxRandom * 0.5)
  return value


inputWidth = 20
print 'param x :='
for i in range(inputWidth):
  print (i + 1), randomValue()
print ';'

for layer in range(numHiddenLayers):
  a = []
  print 'param z' + str(layer) + ' :='
  for i in range(numHiddenUnitsPerLayer):
    zi = randomValue()
    print (i + 1), zi
    a.append(max(zi, 0))
  print ';'
  print ''
  print 'param a' + str(layer) + ' :='
  for i in range(numHiddenUnitsPerLayer):
    print (i + 1), a[i]
  print ';'
  print ''

