all: FEL_INPUT.py FEL_OUTPUT.py duplicates_forward.log duplicates_backward.log


data/GDET_FEE1_241_ENRC.txt:	data/assemble.bash data/GDET_FEE1_241_ENRC.txtaa
	(cd data; ./assemble.bash)

FEL_INPUT.py:	mergeData.py
FEL_OUTPUT.py:	mergeData.py
	python mergeData.py data/BEND*.txt data/QUAD*.txt data/GDET_FEE1_24*.txt

duplicates_forward.log:	FEL_INPUT.py FEL_OUTPUT.py find_duplicates.bash
	./find_duplicates.bash
	mv duplicates.log duplicates_forward.log

removal_candidates_forward.log:	duplicates_forward.log
	egrep "deviation|^#" duplicates_forward.log > removal_candidates_forward.log

remove_duplicates_forward: removal_candidates_forward.log
	python remove_duplicates.py removal_candidates_forward.log FEL_INPUT.py > FEL_INPUT.pynew
	python remove_duplicates.py removal_candidates_forward.log FEL_OUTPUT.py > FEL_OUTPUT.pynew

save_pynew:
	cp FEL_INPUT.pynew FEL_INPUT.py
	cp FEL_OUTPUT.pynew FEL_OUTPUT.py

duplicates_backward.log:	FEL_INPUT.py FEL_OUTPUT.py find_duplicates.bash
	./find_duplicates.bash backward
	mv duplicates.log duplicates_backward.log

clean:
	rm -f FEL_OUTPUT.py FEL_INPUT.py
