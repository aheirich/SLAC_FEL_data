#!/usr/bin/python
#
# forward_inference.py
#

import sys
import math
import numpy
import importlib

VERBOSE = True


model = "ampl_model"
if len(sys.argv) >= 2:
  model = sys.argv[1]
readFromStdin = False
if len(sys.argv) >= 3:
  if sys.argv[2].startswith(stdin):
    readFromStdin = True


if readFromStdin: description = "read from stdin"
else: description = "verify train, test data"
print 'model', model, description

theta = importlib.import_module(model)

if not readFromStdin:
  import FEL_INPUT_SCALED as FEL_INPUT
  import FEL_OUTPUT_SCALED as FEL_OUTPUT


numLayers = theta.numHiddenLayers + 1



def loadModel():
  weights = []
  biases = []
  for i in range(numLayers):
    weights.append(numpy.array(eval('theta.weight_' + str(i))))
    biases.append(numpy.array(eval('theta.bias_' + str(i))))
  return weights, biases




def loadData():
  return FEL_INPUT.train_x, FEL_OUTPUT.train_y, FEL_INPUT.test_x, FEL_OUTPUT.test_y



def printVector(x, name):
  line = name + ' = [ '
  for value in x:
    line = line + str(value) + ', '
    if len(line) > 80:
      print line + '\\'
      line = ''
  print line + ']'




def activations(x, weights, biases):
  if VERBOSE:
    printVector(x, 'x')
  for layer in range(numLayers):
    if layer == 0:
      z = numpy.matmul(x, weights[layer]) + biases[layer]
    else:
      z = numpy.matmul(a, weights[layer]) + biases[layer]
    a = numpy.maximum(z, 0.0)
    if VERBOSE:
      zname = 'z' + str(layer)
      print '# layer', layer, 'preactivations', zname
      printVector(z, zname)
      aname = 'a' + str(layer)
      print '# layer', layer, 'activations', aname
      printVector(a, aname)
  return z



def mse(y0, y1):
  sum = 0.0
  for i in range(len(y0)):
    diff = y0[i] - y1[i]
    sum = sum + diff * diff
  result = sum / len(y0)
  return result




def verify(x, y, weights, biases):
  sse_total = 0.0
  for i in range(len(x)):
    y_computed = activations(x[i], weights, biases)
    mse_i = mse(y_computed, y[i])
    sse_total = sse_total + mse_i * len(y[i])
    print '=== mse', mse_i
    print '=== input:', x[i]
    print '=== output:', y_computed
    print '=== target:', y[i]
    print ''
  result = sse_total / (len(x) * len(y[0]))
  return result




def infer(x, weights, biases):
  for i in range(len(x)):
    y_computed = activations(x[i], weights, biases)
    print '=== input:', x[i]
    print '=== output:', y_computed
    print ''



print 'loadModel'
weights, biases = loadModel()

if readFromStdin:
  for line in sys.stdin:
    line = line.strip()
    eval("infer ([" + line + "], weights, biases)")
else:
  train_x, train_y, test_x, test_y = loadData()
  mse_train = verify(train_x, train_y, weights, biases)
  mse_test = verify(test_x, test_y, weights, biases)
  print 'mse_train', mse_train, 'mse_test', mse_test
