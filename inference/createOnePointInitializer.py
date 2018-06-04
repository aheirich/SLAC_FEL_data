#!/usr/bin/python
#
# createOnePointInitializer
#
# prior to this, generate onepoint.py from the output of verify_forward_inference.py
# with VERBOSE=True
#

import sys

import onepoint as O



def writeInitializer(name, array, file):
  file.write('param ' + name + ':=\n')
  for i in range(len(array)):
    file.write(str(i + 1) + ' ' + str(array[i]) + '\n')
  file.write(';\n\n')


datfile = open("onepoint_initializer.dat", "w")
for name in [ 'x', 'z0', 'a0', 'z1', 'a1', 'z2']:
  writeInitializer(name, eval('O.' + name), datfile)
datfile.close()
