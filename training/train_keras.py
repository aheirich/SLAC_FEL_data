#!/usr/bin/python
#
# train-keras.py
#
# numLayers numUnitsPerLayer learningRate epochs initialEpoch optimizer filenameRoot [checkpoint]
#
#   2 2048 0.00001 10000 0 SGD forward modelname_2_2048_ $SCRATCH/checkpoint/forward_2_2048
#

from sys import argv
import numpy
from keras.models import Sequential
from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import BatchNormalization
from keras.losses import mse
from keras import optimizers
from keras.callbacks import ModelCheckpoint
import FEL_INPUT_SCALED as FEL_INPUT
import FEL_OUTPUT_SCALED as FEL_OUTPUT

repeatableResult = False
usingTensorflow = True
usingBatchNormalization = False

if repeatableResult:
  numpy.random.seed(1)
  if usingTensorflow:
    from tensorflow import set_random_seed
    set_random_seed(2)

numHiddenLayers = 2
numHiddenUnitsPerLayer = 1024
batch_size = 128
epochs = 1000
initialEpoch = 0
learningRate = 0.1
optimizer = "Adadelta"
checkpoint = None
checkpointInterval = 1000

if len(argv) >= 3:
  numHiddenLayers = int(argv[1])
  numHiddenUnitsPerLayer = int(argv[2])
if len(argv) >= 4:
  learningRate = float(argv[3])
if len(argv) >= 5:
  epochs = int(argv[4])
if len(argv) >= 6:
  initialEpoch = int(argv[5])
if len(argv) >= 7:
  optimizer = argv[6]
if len(argv) >= 8:
  filenameRoot = argv[7]
if len(argv) >= 9:
  checkpoint = argv[8]

print('numHiddenLayers', numHiddenLayers, 'unitsPerLayer', numHiddenUnitsPerLayer, 'learningRate', learningRate, 'epochs', epochs, 'initialEpoch', initialEpoch)
if checkpoint is not None:
  print 'continue from checkpoint', checkpoint
print('output to files', filenameRoot)

model = Sequential()

for i in range(numHiddenLayers):
  if i == 0:
    model.add(Dense(numHiddenUnitsPerLayer, activation='relu', input_dim=len(FEL_INPUT.train_x[0])))
  else:
    model.add(Dense(numHiddenUnitsPerLayer, activation='relu'))
  if usingBatchNormalization:
    model.add(BatchNormalization(axis=1))

model.add(Dense(len(FEL_OUTPUT.train_y[0]), activation='linear'))

model.compile(loss=mse, optimizer=eval("optimizers." + optimizer + '(lr=learningRate)'), metrics=['accuracy'])


# checkpoint
filepath = filenameRoot + "-weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
callbacks_list = [ ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min') ]

if checkpoint is not None:
  model.load_weights(checkpoint)


model.fit(FEL_INPUT.train_x, FEL_OUTPUT.train_y,
        batch_size=batch_size,
        epochs=epochs,
        initial_epoch=initialEpoch,
        callbacks=callbacks_list,
        verbose=1,
        validation_data=(FEL_INPUT.train_x, FEL_OUTPUT.train_y))
score = model.evaluate(FEL_INPUT.test_x, FEL_OUTPUT.test_y, verbose=0)
print 'score', score


