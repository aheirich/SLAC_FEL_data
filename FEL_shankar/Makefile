SOURCEFILES=$(wildcard data/BEND_*.txt) $(wildcard data/QUAD_*.txt)
GDET=data/GDET_FEE1_241_ENRC.txt data/GDET_FEE1_242_ENRC.txt
SRTFILES=$(SOURCEFILES:.txt=.srt) $(GDET:.txt=.srt)
SHELL=/bin/bash


all:	FEL_INPUT.py duplicates_forward.log duplicates_backward.log

%.txt:	%.txtaa
	cat $@?* > $@

%.srt:	%.txt rewriteDates.py
	cat $< | python rewriteDates.py | sort > $@

FEL_INPUT.py:	mergeData.py $(SRTFILES)
	python mergeData.py $(SRTFILES)

FEL_INPUT_MONTHLY.py:	mergeDataByMonth.py $(SRTFILES)
	python mergeDataByMonth.py $(SRTFILES)

duplicates_forward.log:	FEL_INPUT.py find_duplicates.bash
	./find_duplicates.bash
	mv duplicates.log duplicates_forward.log

removal_candidates_forward.log:	duplicates_forward.log
	egrep "deviation|^#" duplicates_forward.log > removal_candidates_forward.log

remove_duplicates_forward: removal_candidates_forward.log
	python remove_duplicates.py removal_candidates_forward.log FEL_INPUT.py > FEL_INPUT.pynew
	python remove_duplicates.py removal_candidates_forward.log FEL_OUTPUT.py > FEL_OUTPUT.pynew

save_pynew:	FEL_INPUT.pynew
	cp FEL_INPUT.pynew FEL_INPUT.py
	cp FEL_OUTPUT.pynew FEL_OUTPUT.py

duplicates_backward.log:	FEL_INPUT.py FEL_OUTPUT.py find_duplicates.bash
	./find_duplicates.bash backward
	mv duplicates.log duplicates_backward.log

clean:
	rm -f FEL_OUTPUT.py FEL_INPUT.py
	rm -f $(SRTFILES)
	rm -f $(GDET)
	rm -f duplicate_outputs.txt duplicate_outputs_uniq.txt duplicates_backward.log
	rm -f duplicates_forward.log duplicates.log duplicates.txt duplicate_timestamps.txt
	rm -f input.txt
