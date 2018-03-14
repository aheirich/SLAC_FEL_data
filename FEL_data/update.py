#!/usr/bin/python
#
# carry values forward
#

import string
import fileinput

previous = []
inputs = ['QUAD_LTU1', 'QUAD_L125', 'charge', 'current']
outputs = ['BEND_DMP1_400_BDES', 'GDET_FEE1_241_ENRCHSTBR']
strings = ['ts_str']

def isString(key):
  for s in strings:
    if key.startswith(s):
      return True
  return False

def wantValue(key):
  for i in inputs:
    if key.startswith(i):
      return True
  for o in outputs:
    if key.startswith(o):
      return True
  if isString(key):
    return True
  return False

def convertString(value):
  result = ''
  for c in value:
    if c >= ' ':
      result = result + c
  return '"' + result + '"'


for line in fileinput.input():
  if line.startswith('df_pickles'):
    print "time range", line
    continue
  if line.startswith('keys:'):
    keys = line.split(' ')[1:]
    string = ''
    for key in keys:
      if wantValue(key):
        string = string + key + ' '
    print string
    continue
  if line.startswith('quads:'):
    quads = line.split(' ')[1:]
    continue
  values = line.split(',')
  if len(previous) < 1:
    previous = values
  for i in range(len(values)):
    if values[i] == 'nan':
      values[i] = previous[i]
  string = ""
  for i in range(len(values)):
    key = keys[i]
    value = values[i]
    if isString(key):
      value = convertString(value)
    if wantValue(key):
      string = string + value + ', '
  print string
  previous = values
