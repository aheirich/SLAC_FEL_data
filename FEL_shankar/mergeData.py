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
        datetime = words[0]
        value = words[1]
        if value == 'NaN': continue
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
    value = float(input[1])
    if isInput and isControl(files[i].name):
      data.append(value)
    elif not isInput and not isControl(files[i].name):
      data.append(value)
  return data



def isInteresting(name, datetime):
  if name.startswith('data/GDET') and datetime >= "2017-11-04---18:59:50":
    return True
  return False




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
      datetime = words[0]
      value = words[1]
      if value == 'NaN': continue
      if datetime is None: continue
      if datetime == previousDateTime: continue
      if not isControl(file.name) and (float(value) < 0.1 or float(value) > 7.0): continue # invalid pulse energy values
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

    if lookAhead[i][0] < nextInputs[i][0]:
      print 'ERROR: input is out of order in', file[i].name, 'near', lookAhead[i]

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
FEL_OUTPUT.write('fields = [\\\n')

header = ''
for file in files:
  words = file.name.split('/')
  header = header + '"' + words[1] + '", '

FEL_INPUT.write(header + '\n')
FEL_INPUT.write(']\n')
FEL_INPUT.write('')
FEL_INPUT.write('train_x = numpy.array([\\\n')

FEL_OUTPUT.write(header + '\n')
FEL_OUTPUT.write(']\n')
FEL_OUTPUT.write('')
FEL_OUTPUT.write('train_y = numpy.array([\\\n')


nextInputs = readNext(files)
lookAhead = readNext(files)
controlChanged = True
trainingStartDate = "2017-07-01"
testStartDate = "2017-12-01"
inTest = False
outputSeries = []
printEveryDataPoint = False # debug feature
first = True
lastTime = ''

while True:
  currentTime = latestDateTime(nextInputs)
  inputDisplay = display(currentTime, nextInputs, True, files)
  outputDisplay = display(currentTime, nextInputs, False, files)
  outputSeries.append(outputDisplay)
  nextInputs, lookAhead, controlChanged = getNext(files, currentTime, nextInputs, lookAhead)
  
  stillOpen = False
  for file in files:
    if not file.closed: stillOpen = True
  if not stillOpen: break
  
  if (controlChanged and currentTime >= trainingStartDate) or printEveryDataPoint:
    if currentTime >= testStartDate:
      if not inTest:
        inTest = True
        FEL_INPUT.write('])\n\ntest_x = numpy.array([\\\n')
        FEL_OUTPUT.write('])\n\ntest_y = numpy.array([\\\n')

    if not first:
      FEL_INPUT.write('# ' + str(inputDisplay[0]) + '\n')
      FEL_INPUT.write(str(inputDisplay[1:]) + ', \\\n')
      FEL_INPUT.flush()
      
      FEL_OUTPUT.write('# ' + str(outputDisplay[0]) + '\n')
      smoothedOutputDisplay = smoothed(outputSeries, FEL_OUTPUT)
      FEL_OUTPUT.write(str(smoothedOutputDisplay[1:]) + ', \\\n')
      FEL_OUTPUT.flush()

    outputSeries = []
    first = False

for file in [FEL_INPUT, FEL_OUTPUT]:
  file.write('])\n')
  file.write('')
  file.close()
                     
                     
