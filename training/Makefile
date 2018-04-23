all:	FEL_INPUT_SCALED.py data_statistics.py scaled_statistics.py 

FEL_INPUT_SCALED.py: FEL_INPUT.py FEL_OUTPUT.py rescaleData.py data_statistics.py
	python rescaleData.py data_statistics.py

data_statistics.py: reportDataStatistics.py FEL_INPUT.py FEL_OUTPUT.py
	python reportDataStatistics.py > data_statistics.py

scaled_statistics.py: reportDataStatistics.py FEL_INPUT.py FEL_OUTPUT.py 
	python reportDataStatistics.py scaled > scaled_statistics.py


clean:
	rm -f data_statistics.py scaled_statistics.py
	rm -f FEL_INPUT_SCALED.py FEL_OUTPUT_SCALED.py 

