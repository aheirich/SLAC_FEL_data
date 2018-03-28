#!/usr/bin/python
#
# forward-keras.py
#

import numpy
from keras.models import Sequential
from keras.layers import Conv1D
from keras.layers import Dense
from keras.losses import mse
from keras.optimizers import SGD
import FEL_INPUT
import FEL_OUTPUT

repeatableResult = False
usingTensorflow = True

if repeatableResult:
  numpy.random.seed(1)
  if usingTensorflow:
    from tensorflow import set_random_seed
    set_random_seed(2)

numTrainingSamples = 100000
numHiddenLayers = 2
numHiddenUnitsPerLayer = 1024
batch_size = 128
epochs = 100

print('numHiddenLayers', numHiddenLayers, 'unitsPerLayer', numHiddenUnitsPerLayer, 'batch_size', batch_size, 'epochs', epochs)

model = Sequential()

for i in range(numHiddenLayers):
  if i == 0:
    model.add(Dense(numHiddenUnitsPerLayer, activation='relu', input_dim=len(FEL_INPUT.train_x[0])))
  else:
    model.add(Dense(numHiddenUnitsPerLayer, activation='relu'))

model.add(Dense(len(FEL_OUTPUT.train_y[0]), activation='relu'))

model.compile(loss=mse, optimizer=SGD(lr=0.01),
              metrics=['accuracy'])


model.fit(FEL_INPUT.train_x, FEL_OUTPUT.train_y,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(FEL_INPUT.test_x, FEL_OUTPUT.test_y))

score = model.evaluate(FEL_INPUT.test_x, FEL_OUTPUT.test_y, verbose=0)
print('# score', score)

print('import numpy')

def print1D(array):
  string = '['
  for value in array: string = string + str(value) + ','
  string = string + '],'
  print(string)

def print2D(array):
  for row in array:
    print1D(row)


i = 0
for layer in model.layers:
  weights = layer.get_weights()
  print('layer-' + str(i))
  print('weight_' + str(i) + ' = numpy.array([')
  print1D(weights[0])
  print('])')
  print('')
  print('bias_' + str(i) + ' = numpy.array(')
  print2D(weights[1])
  print(')')
  i = i + 1



