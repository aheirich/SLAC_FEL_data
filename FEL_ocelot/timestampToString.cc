//
// tinmestampToString.cc
//
// convert data file that contains timestamps (seconds since Unix time 0)
// into date-time strings
//

#include <stdio.h>
#include <string.h>
#include <time.h>

const unsigned LINE_SIZE = 4 * 1024;

void convertTimestamp(char line[], unsigned numCommaSkips) {
  char *lastComma = line + strlen(line);
  for(unsigned i = 0; i < numCommaSkips; ++i) {
    lastComma--;
    while(*lastComma != ',') lastComma--;
  }
  char *penultimateComma = lastComma - 1;
  while(*penultimateComma != ',' && penultimateComma > line) {
    penultimateComma--;
  }
  char newline[LINE_SIZE];
  strncpy(newline, line, penultimateComma - line + 1);
  time_t timestamp;
  double doubleTime;
  sscanf(penultimateComma + 1, "%lf", &doubleTime);
  timestamp = (time_t)doubleTime;
  struct tm *ptm;
  ptm = localtime(&timestamp);
  const int baseYear = 1900;
  const int baseMonth = 1;
  sprintf(penultimateComma, ",%04d-%02d-%02d---%02d:%02d:%02d,",
          ptm->tm_year + baseYear, ptm->tm_mon + baseMonth, ptm->tm_mday, ptm->tm_hour, ptm->tm_min, ptm->tm_sec);
}


int main(int argc, char *argv[]) {
  
  unsigned numCommaSkips = 1;
  if(argc > 1) sscanf(argv[1], "%d", &numCommaSkips);
  
  char line[LINE_SIZE];
  unsigned lineCount = 0;
  while(gets(line)) {
    lineCount++;
    // skip first header line
    if(lineCount <= 2) {
      printf("%s\n", line);
      continue;
    }
    convertTimestamp(line, numCommaSkips);
    printf("%s\n", line);
  }
  return 0;
}
