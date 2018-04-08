all:	FEL_INPUT_SCALED.py data_statistics.txt scaled_statistics.txt regularizer.py objective.mod

FEL_INPUT_SCALED.py: FEL_INPUT.py FEL_OUTPUT.py rescaleData.py data_statistics.txt
	python rescaleData.py data_statistics.txt

data_statistics.txt: reportDataStatistics.py
	python reportDataStatistics.py > data_statistics.txt

scaled_statistics.txt: reportDataStatistics.py
	python reportDataStatistics.py scaled > scaled_statistics.txt

regularizer.py:	scaled_statistics.txt
	rm -f regularizer.py
	grep "^min" scaled_statistics.txt | head -1 | sed -e "s/min/input_min = /" >> regularizer.py
	grep "^max" scaled_statistics.txt | head -1 | sed -e "s/max/input_max = /" >> regularizer.py

objective.mod:  regularizer.py
	python makeObjectiveWithRegularizer.py 2
	@echo ASSUMING 2 HIDDEN LAYERS, MAKE AMPL REGULARIZER MANUALLY FOR 3 OR MORE LAYERS

clean:
	rm -f data_statistics.txt scaled_statistics.txt
	rm -f FEL_INPUT_SCALED.py FEL_OUTPUT_SCALED.py
	rm -f objectve.mod objective.dat regularizer.py
