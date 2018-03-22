#
# convert a FEL data stream to numpy array
# fill in missing data
#

fields = []
data = {}
unknownValue = 'nan'

import sys
import fileinput


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


def twodigits(x):
  if x < 10: return '0' + str(x)
  return str(x)


def dateTimeKey(date, time, offset):
  dateWords = date.split('/')
  month = dateWords[0]
  day = dateWords[1]
  year = dateWords[2]
  timeWords = time.split(':')
  hour = timeWords[0]
  minute = timeWords[1]
  second = timeWords[2]
  offsetWords = offset.split(':')
  offsetSign = offsetWords[0][0]
  offsetHours = offsetWords[0][1:]
  
  monthNumber = { 'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6,
    'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12 }
  monthMinusOneLen = { 'Jan' : 31, 'Feb' : 31, 'Mar' : 28, 'Apr' : 31, 'May' : 30, 'Jun' : 31,
    'Jul' : 30, 'Aug' : 31, 'Sep' : 31, 'Oct' : 30, 'Nov' : 31, 'Dec' : 30 }

  assert(offsetSign == '-')
  newHour = int(hour) - int(offsetHours)
  newDay = int(day)
  newMonth = monthNumber[month]
  if newHour < 0:
    newHour = newHour + 24
    newDay = newDay - 1
    if newDay < 0:
      newDay = newDay + monthMinusOneLen[month]
      newMonth = newMonth - 1
  newDate = year + '-' + str(monthNumber[month]) + '-' + day
  newTime = twodigits(newHour) + ':' + minute + ':' + second
  key = newDate + '---' + newTime
  return key



def recordData(date, time, offset, value, fields, data):
  key = dateTimeKey(date, time, offset)
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
  header  = ' , ' + ','.join(fields)
  print 'keys = [ ' + header + ']'
  print 'data = ['
  for key in sorted(data.keys()):
    row = ','.join(data[key])
    print '[' + key + ',' + row + '],'
  print ']'


for line in fileinput.input():
  words = line.split(' ')
  
  if words[0] == 'FIELD':
    ensureUniformRowLength(fields, data)
    field = remove_control_chars(words[1])
    fields.append(field)
    continue
  
  date = words[0].strip()
  time = words[1].strip()
  offset = words[2].strip()
  value = float(words[3].strip())
  recordData(date, time, offset, value, fields, data)

ensureUniformRowLength(fields, data)
propagateForward(data)
reportData(fields, data)

