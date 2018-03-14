
all:	fourFieldsTimestamped.csv

ocelotscrapes:	ocelotscrapes.zip
	mkdir -p ocelotscrapes
	cd ocelotscrapes ; unzip ../ocelotscrapes.zip

data.log:	extract.py ocelotscrapes
	python extract.py > data.log

fourFields.csv:	data.log
	cat data.log | python selectFourFields.py > fourFields.csv

timestampToString:  timestampToString.cc
	g++ -o timestampToString timestampToString.cc

fourFieldsTimestamped.csv:  fourFields.csv timestampToString
	cat fourFields.csv | ./timestampToString > fourFieldsTimestamped.csv

clean:
	rm -rf data.log fourFields.csv ocelotscrapes timestampToString fourFieldsTimestamped.csv

