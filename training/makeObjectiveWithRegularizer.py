#!/usr/bin/python
#
# makeAmplRegularizer.py
#

import sys
import regularizer

if len(sys.argv) == 2:
  outputLayer = sys.argv[1]
else:
  print 'provide the number of layers in the network'
  sys.exit(1)

midpoint = []
halflength = []

for i in range(len(regularizer.input_min)):
  mi = regularizer.input_min[i]
  ma = regularizer.input_max[i]
  midpoint.append((mi + ma) / 2)
  halflength.append((ma - mi) / 2)

modfile = open("objective.mod", "w")
datfile = open("objective.dat", "w")

modfile.write("param regularizer_midpoint{i in 1.." + str(len(midpoint)) + "};\n")
datfile.write("param regularizer_midpoint :=\n")
for i in range(len(midpoint)):
  datfile.write(str(i + 1) + " " + str(midpoint[i]) + "\n")
datfile.write(";\n\n")

modfile.write("param regularizer_halflength{i in 1.." + str(len(halflength)) + "};\n")
datfile.write("param regularizer_halflength :=\n")
for i in range(len(midpoint)):
  datfile.write(str(i + 1) + " " + str(halflength[i]) + "\n")
datfile.write(";\n\n")

modfile.write("# objective function with regularizer\n")
modfile.write("minimize loss: sum{i in 1..columns_" + str(outputLayer) + "}(y_target[i] - a" + str(outputLayer) + "[i])^2")
regularizerExpression = "((x[i] - regularizer_midpoint[i]) / regularizer_halflength[i])^2"
modfile.write(" + sum{i in 1..rows_0}" + regularizerExpression + ";\n")


modfile.close()
datfile.close()
