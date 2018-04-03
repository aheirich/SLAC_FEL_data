#!/usr/bin/python
#
# train-keras.py
#
# numLayers numUnitsPerLayer learningRate epochs direction filenameRoot
#
#   2 2048 0.00001 10000 forward modelname_2_2048_
#

from sys import argv
import numpy
from keras.models import Sequential
from keras.layers import Conv1D
from keras.layers import Dense
from keras.losses import mse
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
import FEL_INPUT
import FEL_OUTPUT

repeatableResult = True
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
learningRate = 0.00001
direction = 'forward'

if len(argv) >= 3:
  numHiddenLayers = int(argv[1])
  numHiddenUnitsPerLayer = int(argv[2])
if len(argv) >= 4:
  learningRate = float(argv[3])
if len(argv) >= 5:
  epochs = int(argv[4])
if len(argv) >= 6:
  direction = argv[5]

filenameRoot = direction + "_" + str(numHiddenLayers) + "_" + str(numHiddenUnitsPerLayer)
if len(argv) >= 7:
  filenameRoot = argv[6]

print('numHiddenLayers', numHiddenLayers, 'unitsPerLayer', numHiddenUnitsPerLayer, 'learningRate', learningRate, 'epochs', epochs, 'direction', direction)
if direction == 'forward':
  print('learning forward mapping from controls to FEL pulse energy')
else:
  print('learning backward mapping from FEL pulse energy to controls')
print('output to files', filenameRoot)

model = Sequential()

numInputLayers = 1
for i in range(numInputLayers + numHiddenLayers):
  if i == 0:
    if direction == 'forward':
      model.add(Dense(numHiddenUnitsPerLayer, activation='relu', input_dim=len(FEL_INPUT.train_x[0])))
    else:
      model.add(Dense(numHiddenUnitsPerLayer, activation='relu', input_dim=len(FEL_INPUT.train_y[0])))
  else:
    model.add(Dense(numHiddenUnitsPerLayer, activation='relu'))

if direction == 'forward':
  model.add(Dense(len(FEL_OUTPUT.train_y[0]), activation='relu'))
else:
  model.add(Dense(len(FEL_OUTPUT.train_x[0]), activation='relu'))

model.compile(loss=mse, optimizer=SGD(lr=learningRate, decay=1.0e-6), metrics=['accuracy'])

# checkpoint
filepath = filenameRoot + "-weights-improvement-{epoch:02d}-{val_acc:.2f}.dat"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]


if direction == 'forward':
  model.fit(FEL_INPUT.train_x, FEL_OUTPUT.train_y,
          batch_size=batch_size,
          epochs=epochs,
          callbacks=callbacks_list,
          verbose=1,
          validation_data=(FEL_INPUT.test_x, FEL_OUTPUT.test_y))
  score = model.evaluate(FEL_INPUT.test_x, FEL_OUTPUT.test_y, verbose=0)
else:
  model.fit(FEL_INPUT.train_y, FEL_OUTPUT.train_x,
          batch_size=batch_size,
          epochs=epochs,
          callbacks=callbacks_list,
          verbose=1,
          validation_data=(FEL_INPUT.test_y, FEL_OUTPUT.test_x))
  score = model.evaluate(FEL_INPUT.test_y, FEL_OUTPUT.test_x, verbose=0)



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





datfileName = filenameRoot + ".dat"
datfile = open(datfileName, "w")
modfileName = filenameRoot + '.mod'
modfile = open(modfileName, "w")
pyfileName = filenameRoot + '.py'
pyfile = open(pyfileName, "w")

datfile.write( '# score' + str(score) + '\n')
datfile.write("# numHiddenLayers " + str(numHiddenLayers) + " numHiddenUnitsPerLayer " + str(numHiddenUnitsPerLayer) + "\n")
modfile.write( '# score' + str(score) + '\n')
modfile.write("# numHiddenLayers " + str(numHiddenLayers) + " numHiddenUnitsPerLayer " + str(numHiddenUnitsPerLayer) + "\n")
pyfile.write( '# score' + str(score) + '\n')
pyfile.write("# numHiddenLayers " + str(numHiddenLayers) + " numHiddenUnitsPerLayer " + str(numHiddenUnitsPerLayer) + "\n")
pyfile.write('import numpy\n')

modfile.write( '\n#\n')
modfile.write( 'param numHiddenLayers;\n')
modfile.write( 'param numHiddenUnitsPerLayer;\n')

datfile.write( '\n#\n')
datfile.write( 'param numHiddenLayers := ' + str(numHiddenLayers) + ';\n')
datfile.write( 'param numHiddenUnitsPerLayer := ' + str(numHiddenUnitsPerLayer) + ';\n')

pyfile.write('\n')
pyfile.write('numHiddenLayers = ' + str(numHiddenLayers) + '\n')
pyfile.write('numHiddenUnitsPerLayer = ' + str(numHiddenUnitsPerLayer) + '\n')


outputSize = len(model.layers[-1].get_weights()[0][0])
modfile.write('\nparam y_target{i in 1..' + str(outputSize) + '};\n\n')

i = 0
for layer in model.layers:
  weights = layer.get_weights()

  modfile.write( '\n# layer-' + str(i) + '\n')
  datfile.write( '\n# layer-' + str(i) + '\n')
  pyfile.write('\n# layer-' + str(i) + '\n')

  rows = len(weights[0])
  columns = len(weights[0][0])
  modfile.write( 'param rows_' + str(i) + ';\n')
  modfile.write( 'param columns_' + str(i) + ';\n')
  datfile.write( 'param rows_' + str(i) + ' := ' + str(rows) + ';\n')
  datfile.write( 'param columns_' + str(i) + ' := ' + str(columns) + ';\n')
  pyfile.write( 'rows_' + str(i) + ' = ' + str(rows) + '\n')
  pyfile.write( 'columns_' + str(i) + ' = ' + str(columns) + '\n')

  modfile.write( 'param weight_' + str(i) + '{i in 1..rows_' + str(i) + ', j in 1..columns_' + str(i) + '};\n')
  datfile.write( 'param weight_' + str(i) + ': ')
  for j in range(columns): datfile.write( str(j + 1) + ' ')
  datfile.write( ':=\n')
  print2D(datfile, weights[0])
  pyfile.write('weight_' + str(i) + ' = [\n')
  for weight in weights[0]:
    pyfile.write('[ ')
    for value in weight:
      pyfile.write(str(value) + ', ')
    pyfile.write(']\n')
  pyfile.write(']\n')

  modfile.write( 'param bias_columns_' + str(i) + ';\n')
  datfile.write( 'param bias_columns_' + str(i) + ' := ' + str(len(weights[1])) + ';\n')
  modfile.write( 'param bias_' + str(i) + '{i in 1..bias_columns_' + str(i) + '};\n')
  datfile.write( 'param bias_' + str(i) + ' :=\n')
  print1D(datfile, weights[1])
  pyfile.write('\nbias_' + str(i) + ' = [ ')
  for value in weights[1]:
    pyfile.write(str(value) + ', ')
  prfile.write(']\n')

  modfile.write('# activations\n')
  modfile.write('var a' + str(i) + '{i in 1..columns_' + str(i) + '};\n\n')

  if i > 0:
    modfile.write('# preactivations\n')
    modfile.write('var z' + str(i) + '{i in 1..columns_' + str(i) + '};\n\n')
    modfile.write('# range constraints\n')
    modfile.write('subject to rangemax' + str(i) + '{i in 1..columns_' + str(i) + '}: z' + str(i) + '[i] <= 1;\n')
    modfile.write('subject to rangemin' + str(i) + '{i in 1..columns_' + str(i) + '}: z' + str(i) + '[i] >= -1;\n')
    modfile.write('\n# compute preactivations\n')
    modfile.write('subject to preactivation' + str(i) + '{i in 1..columns_' + str(i) + '}:\n')
    modfile.write('  z' + str(i) + '[i] = sum{j in 1..columns_' + str(i - 1) + '} (weight_' + str(i) + '[j, i] * z' + str(i - 1) + '[j]) + bias_' + str(i) + '[i];\n')
    modfile.write('\n# compute activations\n')
    modfile.write('subject to activation' + str(i) + '{i in 1..columns_' + str(i) + '}:\n')
    modfile.write('  a' + str(i) + '[i] = z' + str(i) + '[i] * (tanh(100.0*z' + str(i) + '[i]) + 1) * 0.5;\n')

  i = i + 1

modfile.write('\n# output layer constraint\n')
outputLayer = len(model.layers) - 1
modfile.write('subject to zclampPositive' + str(outputLayer) + '{i in 1..columns_' + str(outputLayer) + '}:\n')
modfile.write('  z' + str(outputLayer) + '[i] = if y_target[i] > 0 then y_target[i] else z' + str(outputLayer) + '[i];\n')
modfile.write('subject to zclampNegative' + str(outputLayer) + '{i in 1..columns_' + str(outputLayer) + '}:\n')
modfile.write('  z' + str(outputLayer) + '[i] <= if y_target[i] > 0 then z' + str(outputLayer) + '[i] else 0;\n')

modfile.close()
datfile.close()
pyfile.close()
