#!/bin/bash
for F in GDET*.txtaa
do
  FIELD=`echo ${F} | sed -e "s/.txtaa//"`
  echo ${FIELD}
  cat ${FIELD}.txt?* > ${FIELD}.txt
done
wc -l GDET*.txt
