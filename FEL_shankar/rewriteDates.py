#!/usr/bin/python
#
# rewriteDates.py
#
# rewrite dates into sortable form
#

import sys


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




for line in sys.stdin:
  line = line.strip()
  words = line.split(' ')
  if len(words) == 7:
    dateTime = dateTimeKey(words[0], words[1], words[2])
    output = [dateTime] + words[3:]
    print ' '.join(output)

