all:	model_1_128.mod model_1_128.dat

model_1_128.mod: fel_input.py
	source train_sherlock.bash

fel_input.py: FEL_INPUT.py
	cat FEL_INPUT.py | sed -e "s/[][\\,]//g" > fel_input.py


duplicates.txt: FEL_INPUT.py 
	grep "^\[" FEL_INPUT.py \
	  | sed -e "s/[][\\,]//g" \
	  | sort -n \
	  | uniq -d \
	  > duplicates.txt

duplicates.log: duplicates.txt FEL_OUTPUT.py fel_input.py
	rm -f duplicates.log
	while read duplicate ; \
	do \
	  echo ${duplicate} ; \
	  grep -B 1 "${duplicate}" fel_input.py | grep "^#" | sort > duplicate_timestamps.txt ; \
	  while read duplicate_timestamp ; \
	  do \
	    echo === compare these values, do they differ? if yes the data is not a function >> duplicates.log ; \
	    grep -A 1 "${duplicate_timestamp}" FEL_OUTPUT.py >> duplicates.log ; \
	  done < duplicate_timestamps.txt ; \
	done < duplicates.txt

clean:
	rm -f duplicates.txt duplicates.log fel_input.py duplicate_timestamps.txt
