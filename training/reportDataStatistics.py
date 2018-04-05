#!/usr/bin/python
#
# reportDataStatistics.py
#
# statistics are used for rescaling the data between min and max,
# and standard deviation is used to devide when training error is low enough
#

import math
import sys

if len(sys.argv) > 1 and sys.argv[1].startswith('scale'):
  import FEL_INPUT_SCALED as FEL_INPUT
  import FEL_OUTPUT_SCALED as FEL_OUTPUT
else:
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



def computeStatistics(array):
  sum = []
  for i in range(len(array[0])): sum.append(0.0)
  for row in array:
    for i in range(len(row)):
      sum[i] = sum[i] + row[i]
  mean = []
  for i in range(len(array[0])): mean.append(sum[i] / len(array))
  sumSquares = []
  for i in range(len(array[0])): sumSquares.append(0.0)
  for row in array:
    for i in range(len(row)):
      diff = row[i] - mean[i]
      sumSquares[i] = sumSquares[i] + diff * diff
  stddev = []
  for value in sumSquares: stddev.append(math.sqrt(sumSquares[i] / len(array)))
  return mean, stddev



input_train_min, input_train_max = findRange(FEL_INPUT.train_x)
input_train_mean, input_train_stddev = computeStatistics(FEL_INPUT.train_x)
print ''
print 'input_train', 'min', input_train_min, 'max', input_train_max
print ' mean', input_train_mean
print ' standard deviation', input_train_stddev

input_test_min, input_test_max = findRange(FEL_INPUT.test_x)
input_test_mean, input_test_stddev = computeStatistics(FEL_INPUT.test_x)
print ''
print 'input_test', 'min', input_test_min, 'max', input_test_max
print ' mean', input_test_mean
print ' standard deviation', input_test_stddev

output_train_min, output_train_max = findRange(FEL_OUTPUT.train_y)
output_train_mean, output_train_stddev = computeStatistics(FEL_OUTPUT.train_y)
print ''
print 'output_train', 'min', output_train_min, 'max', output_train_max
print ' mean', output_train_mean
print ' standard deviation', output_train_stddev

output_test_min, output_test_max = findRange(FEL_OUTPUT.test_y)
output_test_mean, output_test_stddev = computeStatistics(FEL_OUTPUT.test_y)
print ''
print 'output_test', 'min', output_test_min, 'max', output_test_max
print ' mean', output_test_mean
print ' standard deviation', output_test_stddev
