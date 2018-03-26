all: FEL_DATA.py

data/GDET_FEE1_241_ENRC.txt:	data/assemble.bash data/GDET_FEE1_241_ENRC.txtaa
	(cd data; ./assemble.bash)

FEL_DATA.py:	data/GDET_FEE1_241_ENRC.txt dataToNumpy.py
	python dataToNumpy.py data/*.txt | tee FEL_DATA.py
