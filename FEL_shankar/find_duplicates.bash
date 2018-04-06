#!/bin/bash
#
# find_duplicates.bash
#
# check FEL_INPUT and FEL_OUTPUT to ensure the data is actually a function
#

DIRECTION=forward
if [[ "$1" != "" ]]
then
  DIRECTION=$1
fi

if [[ "${DIRECTION}" == "forward" ]]
then
  INPUT=FEL_INPUT.py
  OUTPUT=FEL_OUTPUT.py
else
  INPUT=FEL_OUTPUT.py
  OUTPUT=FEL_INPUT.py
fi

LOGFILE=duplicates.log

echo === comparing input ${INPUT} and output ${OUTPUT} to ensure the data is a function
echo === compute the standard deviation of duplicated output values
echo === output to ${LOGFILE}


rm -f input.txt
rm -f ${LOGFILE}

cat ${INPUT} | sed -e "s/[][\\,]//g" > input.txt

grep "^\[" ${INPUT} \
	  | sed -e "s/[][\\,]//g" \
	  | sort -n \
	  | uniq -d \
	  > duplicates.txt

while read duplicate ; do

  echo === for this duplicated input >> ${LOGFILE}
  echo ${duplicate} >> ${LOGFILE}
  dup=`echo "${duplicate}" | sed -e 's/-/\\\\-/g'`

  echo === found these timestamps >> ${LOGFILE}
  grep -B 1 "${dup}" input.txt | grep "^#" | sort > duplicate_timestamps.txt
  cat duplicate_timestamps.txt >> ${LOGFILE}
  wc -l duplicate_timestamps.txt >> ${LOGFILE}

  rm -f duplicate_outputs.txt
  while read duplicate_timestamp ; do
    grep -A 1 "${duplicate_timestamp}" ${OUTPUT} | grep -v "^#" | sed -e "s/[][\\,']//g" >> duplicate_outputs.txt
  done <duplicate_timestamps.txt
  cat duplicate_outputs.txt | sort | uniq > duplicate_outputs_uniq.txt

  echo === These are the duplicated outputs >> ${LOGFILE}
  cat duplicate_outputs_uniq.txt >> ${LOGFILE}
  cat duplicate_outputs_uniq.txt | python duplicate_error.py >> ${LOGFILE}
  echo === >> ${LOGFILE}

done <duplicates.txt


