#
# joinData.py
#
# join the results from archive and ocelot data sources
# match by time and date
# discard nonmatching records
#

import sys

archiveFile = open("../FEL_archive/data.csv", "r")
ocelotFile = open("../FEL_ocelot/selectedFields.csv", "r")

ocelotLines = 0
archiveLines = 0
matches = 0
quadMismatches = 0
discardedArchive = 0
discardedOcelot = 0
ocelotFirst = True
ocelotPrevious = []
archiveWords = ['']
archiveFirst = True
datetime = ''

for ocelotLine in ocelotFile:
  ocelotLines = ocelotLines + 1
  
  if ocelotFirst:
    ocelotFirst = False
    continue
  
  ocelotWords = ocelotLine.strip().split(',')
  if len(ocelotPrevious) == 0:
    ocelotPrevious = ocelotWords

  for i in range(len(ocelotWords)):
    if ocelotWords[i] == 'nan':
      ocelotWords[i] = ocelotPrevious[i]

  new_datetime = str(ocelotWords[len(ocelotWords) - 2])
  if new_datetime == datetime: # redundant data
    continue
  datetime = new_datetime
  ocelotPrevious = ocelotWords

  while archiveWords[0] < datetime:
    archiveLine = archiveFile.readline().strip()
    if archiveFirst:
      archiveFirst = False
      continue
    archiveWords = archiveLine.split(',')
    archiveLines = archiveLines + 1
    if archiveWords[0] < datetime:
      discardedArchive = discardedArchive + 1

  if archiveWords[0] == datetime:
    # compare quads for match
    archiveField = 13
    ocelotField = 1
    mismatch = False
    
    for i in range(4):
      archiveQuad = archiveWords[archiveField + i]
      ocelotQuad = ocelotWords[ocelotField + i]
      if archiveQuad != ocelotQuad:
        print "**** quad mismatch at", datetime, "archive", archiveQuad, "ocelot", ocelotQuad
        quadMismatches = quadMismatches + 1
        mismatch = True
        break

    if not mismatch:
      matches = matches + 1
      for word in ocelotWords:
        archiveWords.append(word)
      string = ','.join(archiveWords)
      print string
  else:
    discardedOcelot = discardedOcelot + 1


print 'ocelot lines', ocelotLines, 'archive lines', archiveLines, 'matches', matches, 'ocelot discards', discardedOcelot, 'archive discards', discardedArchive, 'mismatched quads', quadMismatches
