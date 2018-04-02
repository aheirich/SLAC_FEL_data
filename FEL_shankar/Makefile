all: FEL_INPUT.py FEL_OUTPUT.py


data/GDET_FEE1_241_ENRC.txt:	data/assemble.bash data/GDET_FEE1_241_ENRC.txtaa
	(cd data; ./assemble.bash)

FEL_INPUT.py:	mergeData.py
FEL_OUTPUT.py:	mergeData.py
	python mergeData.py data/BEND*.txt data/QUAD*.txt data/GDET_FEE1_24*.txt

clean:
	rm -f FEL_OUTPUT.py FEL_INPUT.py
