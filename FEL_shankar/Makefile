all:	GDET_FEE1_241_ENRC.txt FEL_DATA.py

GDET_FEE1_241_ENRC.txt:	data/assemble.bash
	(cd data; ./assemble.bash)

FEL_DATA.py:	
	python dataToNumpy.py data/*.txt | tee FEL_DATA.py
