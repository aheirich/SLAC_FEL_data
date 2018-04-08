#!/usr/bin/python
#
# forward_inference.py
#

import sys
import math
import numpy
import importlib



model = "forward_2_2048"
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


numLayers = theta.numHiddenLayers + 2



def loadModel():
  weights = []
  biases = []
  for i in range(numLayers):
    weights.append(numpy.array(eval('theta.weight_' + str(i))))
    biases.append(numpy.array(eval('theta.bias_' + str(i))))
  return weights, biases




def loadData():
  return FEL_INPUT.train_x, FEL_OUTPUT.train_y, FEL_INPUT.test_x, FEL_OUTPUT.test_y




def activations(x, weights, biases):
  for layer in range(numLayers):
    if layer == 0:
      z = numpy.matmul(x, weights[layer]) + biases[layer]
      print 'z' + str(layer), z.shape, '=', x.shape, 'X', weights[layer].shape
      print z
    else:
      z = numpy.matmul(a, weights[layer]) + biases[layer]
      print 'z' + str(layer), z.shape, '=', a.shape, 'X', weights[layer].shape
      print z
    a = numpy.maximum(z, 0.0)
    print 'a' + str(layer) + ' shape', a.shape
    print a
  return a[0]



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
    
    print 'x[i]', x[i]
    print 'y_computed', y_computed
    
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
  print 'loadData'
  train_x, train_y, test_x, test_y = loadData()
  print 'infer train'
  mse_train = verify(train_x, train_y, weights, biases)
  print 'mse_train', mse_train
  print 'infer test'
  mse_test = verify(test_x, test_y, weights, biases)
  print 'mse_test', mse_test
