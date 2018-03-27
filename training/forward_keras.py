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


numTrainingSamples = 100000
numHiddenLayers = 10
numHiddenUnitsPerLayer = 128
batch_size = 128
epochs = 1000


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

score = mode.evaluate(FEL_INPUT.test_x, FEL_OUTPUT.test_y, verbose=0)
print score

print model.parameters()

for layer in len(model.layers):
  weights = layer.get_weights()
  print 'layer'
  print 'weights', weights[0]
  print 'biases', weights[1]

