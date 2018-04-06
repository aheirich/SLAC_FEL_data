#!/usr/bin/python

import sys
import math

array = []
for line in sys.stdin: 
  words = line.strip().split(' ')
  print words
  array.append(words)

sum = []
for i in array[0]: sum.append(0.0)

for words in array:
  for i in range(len(words)):
    sum[i] = sum[i] + float(words[i])

mean = []
for value in sum: mean.append(value / len(array))

sumSquares = 0.0
for words in array:
  for i in range(len(words)):
    diff = float(words[i]) - mean[i]
    sumSquares = sumSquares + diff * diff

standardDeviation = math.sqrt(sumSquares / len(array))
print '=== standard deviation of duplicates is', standardDeviation

