from scipy import *
from scipy.signal import *
from matplotlib.pyplot import *
import parsedata
import datetime
import thinkplot
import numpy

def getDay(day,fulldata):
	# day: datetime date object
	# fulldata: all data
	# returns all data from day

	dstart = datetime.datetime.combine(day,datetime.time(hour=0))
	dend = dstart+datetime.timedelta(days=1)

	data = []
	i = 0
	while fulldata[i][0]<dstart:
		i+=1
	while fulldata[i][0]<=dend:
		data.append(fulldata[i])
		i+=1
	return data

def smoother(data):
	# takes a list of data
	# returns an list one element smaller
	data = array(data)
	n = data.shape[0]
	filt=gaussian( 31,4 )
	filt /= sum( filt )
	padded = concatenate( (data[0]*ones(31//2), data, data[n-1]*ones(31//2)) )
	smooth = convolve( padded, filt, mode='valid')

	return list(smooth)

def getDays(data):
	# takes a list of data
	# returns a list of the days as datetime.date objects
	date,depth,light,temp = zip(*data)
	first = date[0].date()
	last = date[-1].date()
	dif = (last-first).days
	return [ first + datetime.timedelta(days=x) for x in range(0,dif) ]

def getRiseSet(day,fulldata):
	# takes a datetime.day object and a list of data
	# returns a list of (sunrise,sunset) datetime.datetime objects

	# get info for day
	dayData = getDay(day,fulldata)
	date,depth,light,temp = zip(*dayData)

	# smooth data
	light = smoother(light)
	lightdif = []
	index = range(len(light)-1)
	for i in index:
		lightdif.append(light[i+1]-light[i])

	# pull out sunrise/sunset
	changes = (smoother(lightdif),date[0:-1])
	combo = zip(*changes)
	return (min(combo)[1],max(combo)[1])

def allRiseSet(fulldata):
	# takes a continuous data set
	# returns a list of (risetime, settime) as datetime.datetime objects
	days = getDays(fulldata)
	times = []
	for day in days:
		rise,sset = getRiseSet(day,fulldata)
		times.append((rise,sset))
	return times

if __name__=="__main__":
	lightData = parsedata.parseFile("mooring.tab")
	times = allRiseSet(lightData)
	rise,sset=zip(*times)
	timing = [dt.time() for dt in rise]
	d = datetime.datetime.today()
	dtiming = [datetime.datetime.combine(d,t) for t in timing]

	thinkplot.Scatter(range(len(timing)),dtiming)
	thinkplot.Show()