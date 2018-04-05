all:	FEL_INPUT_SCALED.py

FEL_INPUT_SCALED.py: FEL_INPUT.py FEL_OUTPUT.py rescaleData.py
	python rescaleData.py -112 112 -1 28

ranges.txt: findDataRange.py
	python findDataRange.py > ranges.txt

