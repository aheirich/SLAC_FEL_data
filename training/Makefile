all:	FEL_INPUT_SCALED.py data_statistics.txt scaled_statistics.txt

FEL_INPUT_SCALED.py: FEL_INPUT.py FEL_OUTPUT.py rescaleData.py data_statistics.txt
	python rescaleData.py data_statistics.txt

data_statistics.txt: reportDataStatistics.py
	python reportDataStatistics.py > data_statistics.txt

scaled_statistics.txt: reportDataStatistics.py
	python reportDataStatistics.py scaled > scaled_statistics.txt

clean:
	rm -f data_statistics.txt
	rm -f FEL_INPUT_SCALED.py FEL_OUTPUT_SCALED.py

