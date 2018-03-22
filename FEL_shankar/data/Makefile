all:	GDET_DATA

GDET_DATA:
	for field in GDET_FEE1_241_ENRC GDET_FEE1_242_ENRC GDET_FEE1_361_ENRC GDET_FEE1_362_ENRC
	do
		echo ${field}
		cat ${field}.txt?* > ${field}.txt
	done
