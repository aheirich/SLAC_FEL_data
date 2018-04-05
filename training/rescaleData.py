#!/usr/bin/python
#
# rescaleData.py
#

import sys
import FEL_INPUT
import FEL_OUTPUT


def rescale(array, minx, maxx):
  for j in range(len(array)):
    row = array[j]
    for i in range(len(row)):
      value = row[i]
      scaledValue = (value - minx) / (maxx - minx)
      row[i] = scaledValue
    array[j] = row
  return array



def write_array(file, array, name):
  file.write(name + " = numpy.array([\n")
  for row in array:
    file.write("  [ ")
    for value in row:
      file.write(str(value) + ", ")
    file.write("], \\\n")
  file.write("])\n\n")



if len(sys.argv) == 5:
  min_x = float(sys.argv[1])
  max_x = float(sys.argv[2])
  min_y = float(sys.argv[3])
  max_y = float(sys.argv[4])
else:
  print "provide xmin, xmax, ymin, ymax"
  sys.exit(1)

fel_input = open("FEL_INPUT_SCALED.py", "w")
fel_input.write("import numpy\n")
fel_output = open("FEL_OUTPUT_SCALED.py", "w")
fel_output.write("import numpy\n")

fel_input.write("fields = " + str(FEL_INPUT.fields) + "\n\n")

train_x = rescale(FEL_INPUT.train_x, min_x, max_x)
write_array(fel_input, train_x, "train_x")
train_y = rescale(FEL_OUTPUT.train_y, min_y, max_y)
write_array(fel_output, train_y, "train_y")
test_x = rescale(FEL_INPUT.test_x, min_x, max_x)
write_array(fel_input, test_x, "test_x")
test_y = rescale(FEL_OUTPUT.test_y, min_y, max_y)
write_array(fel_output, test_y, "test_y")

fel_input.close()
fel_output.close()

