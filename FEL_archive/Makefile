all:	data.csv

data.log:	getData.py
	python getData.py > data.log

data.csv:	data.log
	cat data.log | python dataLogToCSV.py > data.csv

clean:
	rm -f data.log data.csv
