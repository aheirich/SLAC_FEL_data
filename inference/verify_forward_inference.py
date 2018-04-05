#!/usr/bin/python
#
# forward_inference.py
#

import sys
import math
import numpy

import forward_2_2048
import FEL_INPUT
import FEL_OUTPUT

numLayers = forward_2_2048.numHiddenLayers + 2



def loadModel():
  weights = []
  biases = []
  for i in range(numLayers):
    weights.append(numpy.array(eval('forward_2_2048.weight_' + str(i))))
    biases.append(numpy.array(eval('forward_2_2048.bias_' + str(i))))
  return weights, biases




def loadData():
  return numpy.array(FEL_INPUT.train_x), numpy.array(FEL_OUTPUT.train_y), numpy.array(FEL_INPUT.test_x), numpy.array(FEL_OUTPUT.test_y)




def activations(x, weights, biases):
  for layer in range(len(weights) + 1):
    if layer == 0:
      a = numpy.array(x)
    else:
      aShape = a.shape
      z = numpy.matmul(a, weights[layer - 1]) + biases[layer - 1]
      a = numpy.maximum(z, 0.0)
  return a[0]



def mse(y0, y1):
  sum = 0.0
  for i in range(len(y0)):
    diff = y0[i] - y1[i]
    sum = sum + diff * diff
  result = sum / len(y0)
  return result



def infer(x, y, weights, biases):
  mse_total = 0.0
  for i in range(len(x)):
    y_computed = activations(x[i], weights, biases)
    mse_i = mse(y_computed, y[i])
    mse_total = mse_total + mse_i * len(y[i])
    print '=== mse', mse_i
    print '=== input:', x[i]
    print '=== output:', y_computed
    print '=== target:', y[i]
    print ''
  result = mse_total / (len(x) * len(y[0]))
  return result



print 'w,b'
weights, biases = loadModel()
print 'tx,ty'
train_x, train_y, test_x, test_y = loadData()
print 'mes_train'
mse_train = infer(train_x, train_y, weights, biases)
print 'mse_train', mse_train
mse_test = infer(test_x, test_y, weights, biases)
print 'mse_test', mse_test
