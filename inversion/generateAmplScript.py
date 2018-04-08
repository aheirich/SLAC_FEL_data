#!/usr/bin/python
#
# generateAmplScript.py
#

import sys
import random

if len(sys.argv) == 3:
  numHiddenLayers = int(sys.argv[1])
  numHiddenUnitsPerLayer = int(sys.argv[2])
else:
  print 'please provide numHiddenLayers and numHiddenUnitsPerLayer'
  print 'eg 2 2048'
  sys.exit(1)


modelname = "forward_" + str(numHiddenLayers) + "_" + str(numHiddenUnitsPerLayer)


def randomValue():
  maxRandom = 1000000000
  r = random.randint(0, maxRandom) - (maxRandom / 2)
  value = float(r) / (maxRandom * 0.5)
  return value



randomFileDir = "randomInit/"

def createRandomInitFile(trial):
  random.seed(trial)
  filename = randomFileDir + 'randomInit' + str(trial) + '.dat'
  file = open(filename, "w")
  inputWidth = 20
  file.write("# random init " + str(numHiddenLayers) + " " + str(numHiddenUnitsPerLayer) + " trial " + str(trial) + '\n')
  file.write('param x :=\n')
  for i in range(inputWidth):
    file.write(str(i + 1) + ' ' + str(max(randomValue(), 0)) + '\n')
  file.write(';\n')

  for layer in range(numHiddenLayers):
    a = []
    file.write('param z' + str(layer) + ' :=\n')
    for i in range(numHiddenUnitsPerLayer):
      zi = randomValue()
      file.write(str(i + 1) + ' ' + str(zi) + '\n')
      a.append(max(zi, 0))
    file.write(';\n')
    file.write('\n')
    file.write('param a' + str(layer) + ' :=\n')
    for i in range(numHiddenUnitsPerLayer):
      file.write(str(i + 1) + ' ' + str(a[i]) + '\n')
    file.write(';\n')
    file.write('\n')
  file.close()
  return filename

bashScript = open(modelname + '.bash', 'w')

numTrials = 100
for trial in range(numTrials):
  filename = randomFileDir + modelname + "_" + str(trial) + ".run"
  amplScript = open(filename, 'w')
  amplScript.write('# ::: Trial ' + str(trial) + ' :::\n')
  amplScript.write('model ' + modelname + '.mod;\n')
  amplScript.write('model objective.mod;\n')
  amplScript.write('data ' + modelname + '.dat;\n')
  amplScript.write('data objective.dat;\n')
  amplScript.write('data y_target.dat;\n')
  randomInitFilename = createRandomInitFile(trial)
  amplScript.write('data ' + randomInitFilename + ';\n')
  amplScript.write('option solver "/home/aheirich/bin/ampl.linux64/minos";\n')
  amplScript.write('option minos_options "meminc=535 optimality_tolerance=1.0e-3 feasibility_tolerance=1.0e-3";\n')
  amplScript.write('solve;\n')
  amplScript.write('display x;\n')
  amplScript.write('display a' + str(numHiddenLayers) + ';\n')
  amplScript.write('display z' + str(numHiddenLayers) + ';\n')
  for layer in range(numHiddenLayers):
    amplScript.write('display a' + str(layer) + ';\n')
    amplScript.write('display z' + str(layer) + ';\n')
  amplScript.write('quit;\n')
  amplScript.close()
  bashScript.write('echo Trial ' + str(trial) + '\n')
  bashScript.write('ampl < ' + amplScript.name + '\n')

bashScript.close()

