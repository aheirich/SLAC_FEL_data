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



def isControl(name):
  return not name.startswith('data/GDET') # pulse energy


def display(datetime, nextInputs, isInput, files):
  data = [ datetime ]
  for i in range(len(nextInputs)):
    input = nextInputs[i]
    if isInput and isControl(files[i].name):
      data.append(input[1])
    elif not isInput and not isControl(files[i].name):
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



def smoothed(series, file):
  sum = []
  for i in series[0]: sum.append(0.0)
  counter = 0
  i = 0
  for row in series:
    i = i + 1
    if i <= len(series) / 2: continue
    counter = counter + 1
    for j in range(len(row)):
      if j == 0:
        sum[j] = row[j]
      else:
        sum[j] = sum[j] + float(row[j])
  result = []
  for i in range(len(sum)):
    if i == 0:
      result.append(sum[i])
    else:
      result.append(sum[i] / counter)
  return result




files = openInputFiles(sys.argv[1:])
FEL_INPUT = open('FEL_INPUT.py', 'w')
FEL_OUTPUT = open('FEL_OUTPUT.py', 'w')
FEL_INPUT.write("import numpy\n")
FEL_INPUT.write('fields = [\\\n')
FEL_OUTPUT.write("import numpy\n")
header = ''
for file in files:
  words = file.name.split('/')
  header = header + '"' + words[1] + '", '
FEL_INPUT.write(header + '\n')
FEL_INPUT.write(']\n')
FEL_INPUT.write('')
FEL_INPUT.write('train_x = numpy.array([\\\n')
FEL_OUTPUT.write('train_y = numpy.array([\\\n')

nextInputs = readNext(files)
lookAhead = readNext(files)
lastDisplay = ''
controlChanged = True
trainingStartDate = "2017-07-01"
testStartDate = "2017-12-01"
inTest = False
outputSeries = []
printEveryDataPoint = False # debug feature
first = True

while True:
  currentTime = latestDateTime(nextInputs)
  inputDisplay = display(currentTime, nextInputs, True, files)
  outputDisplay = display(currentTime, nextInputs, False, files)
  outputSeries.append(outputDisplay)
  fullDisplay = inputDisplay + outputDisplay
  if fullDisplay == lastDisplay: break
  lastDisplay = fullDisplay
  nextInputs, lookAhead, controlChanged = getNext(files, currentTime, nextInputs, lookAhead)
  
  if (controlChanged and currentTime >= trainingStartDate) or printEveryDataPoint:
    if currentTime >= testStartDate:
      if not inTest:
        inTest = True
        FEL_INPUT.write('])\n\ntest_x = numpy.array([\\\n')
        FEL_OUTPUT.write('])\n\ntest_y = numpy.array([\\\n')
  
    if not first:
      FEL_INPUT.write('# ' + str(inputDisplay[0]) + '\n')
      FEL_INPUT.write(str(inputDisplay[1:]) + ', \\\n')
      
      FEL_OUTPUT.write('# ' + str(outputDisplay[0]) + '\n')
      smoothedOutputDisplay = smoothed(outputSeries, FEL_OUTPUT)
      FEL_OUTPUT.write(str(smoothedOutputDisplay[1:]) + ', \\\n')

    outputSeries = []
    first = False

for file in [FEL_INPUT, FEL_OUTPUT]:
  file.write('])\n')
  file.write('')
  file.close()
                     
                     
