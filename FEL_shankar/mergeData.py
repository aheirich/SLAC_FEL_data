#
# merge FEL data
#
# every output point occurs just prior to changing a control
# the goal is to get the GDET steady state following each control change
# use these points for training and testing
#

import sys

MAX_DATETIME = "9999-99-99---99:99:99"



def openInputFiles(argv):
  files = []
  for i in range(len(argv)):
    if i != 0:
      file = open(argv[i], "r")
      files.append(file)
  return files


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
    if newDay <= 0:
      newDay = newDay + monthMinusOneLen[month]
      newMonth = newMonth - 1
  newDate = year + '-' + str(twodigits(newMonth)) + '-' + str(twodigits(newDay))
  newTime = twodigits(newHour) + ':' + minute + ':' + second
  key = newDate + '---' + newTime
  return key




def convertLine(line):
  words = line.split(' ')
  date = words[0].strip()
  time = words[1].strip()
  offset = words[2].strip()
  valueWord = words[3].strip()
  if valueWord == 'NaN': return None, None
  value = float(valueWord)
  key = dateTimeKey(date, time, offset)
  return key, value





def latestDateTime(nextInputs):
  maxDateTime = ''
  for input in nextInputs:
    if input != '':
      datetime, value = input
      if datetime > maxDateTime:
        maxDateTime = datetime
  return maxDateTime




def readNext(files):
  result = []
  for file in files:
    while True:
      line = file.readline().strip()
      if line.startswith('FIELD'): continue
      words = line.split(' ')
      if len(words) > 4:
        datetime, value = convertLine(line)
        if datetime is None: continue
        result.append([datetime, value])
        break
  return result



def display(datetime, nextInputs):
  data = [ datetime ]
  for input in nextInputs:
    data.append(input[1])
  return data



def readAhead(file, i, nextInputs, lookAhead, previousDateTime):
  if lookAhead[i][0] != MAX_DATETIME:
    nextInputs[i] = lookAhead[i]

  while not file.closed:
    line = file.readline().strip()
    if len(line) == 0:
      file.close()
      lookAhead[i] = [ MAX_DATETIME, -1 ]
      break
    if line.startswith('FIELD'): continue
    words = line.split(' ')
    if len(words) > 4:
      datetime, value = convertLine(line)
      if datetime is None: continue
      if datetime == previousDateTime: continue
      lookAhead[i] = [datetime, value]
      break
  return nextInputs, lookAhead



def isControl(name):
  return not name.startswith('data/GDET') # pulse energy



def getNext(files, currentTime, nextInputs, lookAhead):
  earliestDateTime = MAX_DATETIME
  controlChanged = False
  
  for i in range(len(files)):
    lookaheadDateTime = lookAhead[i][0]
    if lookaheadDateTime >= currentTime and lookaheadDateTime < earliestDateTime:
      earliestDateTime = lookaheadDateTime
  
  for i in range(len(files)):
    lookaheadDateTime = lookAhead[i][0]
    if lookaheadDateTime == earliestDateTime:
      oldValue = nextInputs[i]
      nextInputs, lookAhead = readAhead(files[i], i, nextInputs, lookAhead, lookaheadDateTime)
      newValue = nextInputs[i]
      valueChanged = oldValue[1] != newValue[1]
      if valueChanged and isControl(files[i].name):
        controlChanged = True

  return nextInputs, lookAhead, controlChanged




print ''
print 'import numpy'
print ''
print 'fields = [ \\'
header = '"DATE_TIME", '

files = openInputFiles(sys.argv)

for file in files:
  words = file.name.split('/')
  header = header + '"' + words[1] + '", '
print header
print ']'
print ''
print 'training_data = numpy.array([ \\'

nextInputs = readNext(files)
lookAhead = readNext(files)
lastOutput = ''
controlChanged = True

while True:
  currentTime = latestDateTime(nextInputs)
  output = display(currentTime, nextInputs)
  if output == lastOutput: break
  lastOutput = output
  nextInputs, lookAhead, controlChanged = getNext(files, currentTime, nextInputs, lookAhead)
  if controlChanged:
    print output, ', \\'
print output

print '])'
print ''

