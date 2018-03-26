#!/bin/bash
for F in GDET*.txtaa
do
  FIELD=`echo ${F} | sed -e "s/.txtaa//"`
  echo ${FIELD}
  echo "FIELD ${FIELD}" > ${FIELD}.all
  cat ${FIELD}.txt?* >> ${FIELD}.all
  mv ${FIELD}.all ${FIELD}.txt
done
wc -l GDET*.txt
