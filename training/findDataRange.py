#!/usr/bin/python
#
# findDataRange.py
#

import sys
import FEL_INPUT
import FEL_OUTPUT


def findRange(array):
  minx = 999999
  maxx = -minx
  for row in array:
    for value in row:
      minx = min(minx, value)
      maxx = max(maxx, value)
  return minx, maxx


input_train_min, input_train_max = findRange(FEL_INPUT.train_x)
print 'input train', input_train_min, input_train_max
input_test_min, input_test_max = findRange(FEL_INPUT.test_x)
print 'input_test', input_test_min, input_test_max
output_train_min, output_train_max = findRange(FEL_OUTPUT.train_y)
print 'output_train', output_train_min, output_train_max
output_test_min, output_test_max = findRange(FEL_OUTPUT.test_y)
print 'output_test', output_test_min, output_test_max
