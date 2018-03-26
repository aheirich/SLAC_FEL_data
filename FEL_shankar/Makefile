all: FEL_DATA.py

data/GDET_FEE1_241_ENRC.txt:	data/assemble.bash data/GDET_FEE1_241_ENRC.txtaa
	(cd data; ./assemble.bash)

FEL_DATA.py:	data/GDET_FEE1_241_ENRC.txt mergeData.py
	python mergeData.py data/*.txt > FEL_DATA.py
