import sys
import urllib2
import json
import numpy
import time as steve # had to do this to make datetime and time get along, since I'm too lazy to find the real solution to the problem. 
from datetime import *
import pytz # python time zone package

############# Methods to deal with parsing date strings and converting time to GMT to be used in the archiver #################
# Determines the year, month, and day from Adam's date string format. Ie.) '2017-05-23T00:00:00'
def find_mon_day(dateString):
    year_num = int(dateString[0:4])
    month_num = int(dateString[dateString.find('-')+1:dateString.find('-')+3])
    day_num = int(dateString[dateString.find('-',dateString.find('-')+1)+1:dateString.find('-',dateString.find('-')+1)+3])
    return year_num,month_num,day_num

# Returns hour, minute, and second data from Adam's date string format
def find_hr_min_sec(dateString):
    hr_num = int(dateString[dateString.find('T')+1:dateString.find('T')+3])
    min_num = int(dateString[dateString.find(':')+1:dateString.find(':')+3])
    sec_num = int(dateString[dateString.find(':',dateString.find(':')+1)+1:])
    return hr_num,min_num,sec_num

# Returns the year, month, day etc. as a tuple to be used in other methods.
def datestr2ints(datestr):
    year,month,day = find_mon_day(datestr)
    hr,minute,sec = find_hr_min_sec(datestr)
    return (year,month,day,hr,minute,sec)

# Evidently, the dates have to be put into the url as GMT not Pacific time to get the correct data and timestamps.
# This converts the user format into GMT.
# Mostly copied from Nora's code
def userTime2gmt(datestr):
    datetuple = datestr2ints(datestr)
    timeAsDatetime = datetime(*datetuple)
    GmtTimeZone= pytz.timezone('GMT') # Greenwich mean time zone object
    LocalTimeZone=pytz.timezone('America/Los_Angeles') #local Pacific time zone object
    localDateTime=LocalTimeZone.localize(timeAsDatetime)#create a date object with a localized timezone for reference
    shiftedTime=localDateTime.astimezone(GmtTimeZone)
    return str(datetime.isoformat(shiftedTime))[:str(datetime.isoformat(shiftedTime)).find('+')]


#######################  Methods to convert archive data to JSON format and then into lists ###########################                      
# Converts urllib data into a numpy array via json...not really sure what json is, but it works! Thanks Adam!
def datArrange(response):
    data = json.load(response)
    realData = data[0]["data"]
    seconds=numpy.array([x.get('secs') for x in realData[:]],dtype =float)
    nanosUse = 1e-9*numpy.array([x.get('nanos') for x in realData[:]], dtype = float)
    value = numpy.array([x.get('val') for x in realData[:]])
    time = numpy.array([sum(x) for x in zip(seconds, nanosUse)],dtype = float)
    return time, value

# Time start and end has to have format: '<year>-<mon>-<day>T<hr>:<min>:<sec>' 
# EX.) '2017-01-01T00:00:00'
def pullData(pv, start, end):
    start = userTime2gmt(start)
    end = userTime2gmt(end)
    response = urllib2.urlopen("http://lcls-archapp.slac.stanford.edu/retrieval/data/getData.json?pv="+pv+"&from="+start+"Z&to="+end+"Z")
    time, value = datArrange(response)
    return time,value





################## Example of use ######################

# base_times is an array of time data in the time-since-epoch format (presumably the time in seconds from the date that the original Star Wars came out) 
# This first example uses a BPM in LI24, but you can change it to whatever you like.
base_times, values =  pullData('BPMS:LI24:601:TMIT1H', '2017-07-01T00:00:01', '2017-07-01T00:00:05')


for i in range(len(base_times)):
    print steve.strftime('%Y-%m-%d %H:%M:%S', steve.localtime(base_times[i])), values[i]
