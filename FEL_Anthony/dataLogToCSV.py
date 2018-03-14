#
# convert a FEL data stream of this form to CSV
#
"""
  FIELD BEND:DMP1:400:BDES
  2017-06-30 21:02:23 14.438
  2017-07-01 01:17:15 14.438
"""

fields = []
data = {}
unknownValue = 'nan'

import sys


def ensureUniformRowLength(fields, data):
  numColumns = len(fields)
  for key in data.keys():
    if len(data[key]) < numColumns:
      assert len(data[key]) == numColumns - 1
      data[key].append(unknownValue)

# https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python

import unicodedata, re

all_chars = (unichr(i) for i in xrange(0x110000))
control_chars = ''.join(c for c in all_chars if unicodedata.category(c) == 'Cc')
# or equivalently and much more efficiently
control_chars = ''.join(map(unichr, range(0,32) + range(127,160)))

control_char_re = re.compile('[%s]' % re.escape(control_chars))

def remove_control_chars(s):
  return control_char_re.sub('', s)

def newDataRow(fields, value):
  row = []
  for i in range(len(fields) - 1):
    row.append(unknownValue)
  row.append(remove_control_chars(str(value)))
  return row


def recordData(date, time, value, fields, data):
  key = date + "T" + time
  if key not in data.keys():
    data[key] = newDataRow(fields, value)
  else:
    if len(data[key]) < len(fields):
      data[key].append(remove_control_chars(str(value)))


def propagateForward(data):
  previous = None
  for key in sorted(data.keys()):
    if previous is None:
      previous = data[key]
      continue
    values = data[key]
    for i in range(len(values)):
      if values[i] == unknownValue:
        values[i] = previous[i]
    data[key] = values
    previous = values


def reportData(fields, data):
  header  = ','.join(fields)
  print header
  for key in sorted(data.keys()):
    row = ','.join(data[key])
    print key + ',' + row


for line in sys.stdin:
  words = line.split(' ')
  
  if words[0] == 'FIELD':
    ensureUniformRowLength(fields, data)
    field = remove_control_chars(words[1])
    fields.append(field)
    continue

  if words[0].startswith('201'):
    date = words[0].strip()
    time = words[1].strip()
    value = float(words[2].strip())
    recordData(date, time, value, fields, data)
  else:
    continue

ensureUniformRowLength(fields, data)
propagateForward(data)
reportData(fields, data)
