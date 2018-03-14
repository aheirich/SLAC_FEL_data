//
// tinmestampToString.cc
//
// convert data file that contains timestamps (seconds since Unix time 0)
// into date-time strings
//

#include <stdio.h>
#include <string.h>
#include <time.h>


void convertTimestamp(char line[]) {
  char *lastComma = line + strlen(line) - 1;
  char *penultimateComma = lastComma - 1;
  while(*penultimateComma != ',' && penultimateComma > line) {
    penultimateComma--;
  }
  char newline[512];
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
  char line[512];
  bool first = true;
  while(gets(line)) {
    // skip first header line
    if(first) {
      first = false;
      printf("%s", line);
      continue;
    }
    convertTimestamp(line);
    printf("%s\n", line);
  }
  return 0;
}
