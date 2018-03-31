#!/usr/bin/python
#
# forward-keras.py
#

from sys import argv
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

if len(argv) == 3:
  numHiddenLayers = int(argv[1])
  numHiddenUnitsPerLayer = int(argv[2])

print('numHiddenLayers', numHiddenLayers, 'unitsPerLayer', numHiddenUnitsPerLayer, 'batch_size', batch_size, 'epochs', epochs)

model = Sequential()

numInputLayers = 1
for i in range(numInputLayers + numHiddenLayers):
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

datfileName = "model_" + str(numHiddenLayers) + "_" + str(numHiddenUnitsPerLayer) + ".dat"
datfile = open(datfileName, "w")
modfileName = "model_" + str(numHiddenLayers) + "_" + str(numHiddenUnitsPerLayer) + ".mod"
modfile = open(modfileName, "w")

datfile.write( '# score' + str(score) + '\n')
datfile.write("# numHiddenLayers " + str(numHiddenLayers) + " numHiddenUnitsPerLayer " + str(numHiddenUnitsPerLayer) + "\n")
modfile.write( '# score' + str(score) + '\n')

modfile.write( '\n')
modfile.write( 'param numHiddenLayers ;\n')
modfile.write( 'param numHiddenUnitsPerLayer ;\n')

datfile.write( '\n')
datfile.write( 'param numHiddenLayers := ' + str(numHiddenLayers) + ' ;\n')
datfile.write( 'param numHiddenUnitsPerLayer := ' + str(numHiddenUnitsPerLayer) + ' ;\n')

def print1D(file, array):
  i = 1
  for value in array: 
    file.write( str(i) + ' ' + str(value) + '\n')
    i = i + 1
  file.write( ';\n\n')

def print2D(file, array):
  i = 1
  for row in array:
    file.write( str(i) + ' ')
    for value in row: file.write( str(value) + ' ')
    file.write( '\n')
    i = i + 1
  file.write( ';\n\n')


modfile.write('# len(model.layers) = ' + str(len(model.layers)) + '\n')

i = 0
for layer in model.layers:
  weights = layer.get_weights()

  modfile.write( '# layer-' + str(i) + '\n')
  datfile.write( '# layer-' + str(i) + '\n')

  rows = len(weights[0])
  columns = len(weights[0][0])
  modfile.write( 'param rows_' + str(i) + ';\n')
  modfile.write( 'param columns_' + str(i) + ';\n')
  datfile.write( 'param rows_' + str(i) + ' := ' + str(rows) + ';\n')
  datfile.write( 'param columns_' + str(i) + ' := ' + str(columns) + ';\n')

  modfile.write( 'param weight_' + str(i) + '{i in 1..rows_' + str(i) + ', j in 1..columns_' + str(i) + '};\n')
  datfile.write( 'param weight_' + str(i) + ': ')
  for j in range(columns): datfile.write( str(j + 1) + ' ')
  datfile.write( ':=\n')
  print2D(datfile, weights[0])

  modfile.write( 'param bias_columns_' + str(i) + ';\n')
  datfile.write( 'param bias_columns_' + str(i) + ' := ' + str(len(weights[1])) + ';\n')
  modfile.write( 'param bias_' + str(i) + '{i in 1..bias_columns_' + str(i) + '};\n')
  datfile.write( 'param bias_' + str(i) + ' :=\n')
  print1D(datfile, weights[1])
  i = i + 1

modfile.close()
datfile.close()





