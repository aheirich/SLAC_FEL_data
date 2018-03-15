
all:	selectedFields.csv

ocelotscrapes:	ocelotscrapes.zip
	mkdir -p ocelotscrapes
	cd ocelotscrapes ; unzip ../ocelotscrapes.zip

data.log:	extract.py ocelotscrapes
	python extract.py > data.log

data_timestamped.log: data.log timestampToString
	cat data.log | ./timestampToString 2 > data_timestamped.log

selectedFields.csv:	data_timestamped.log
	cat data_timestamped.log | python selectFields.py > selectedFields.csv

timestampToString:  timestampToString.cc
	g++ -g -o timestampToString timestampToString.cc


clean:
	rm -rf data.log selectedFields.csv ocelotscrapes timestampToString

