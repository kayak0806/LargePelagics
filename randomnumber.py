from datetime import timedelta, datetime, date
import datetime
import random
import scipy.stats as stats
import thinkplot as tp
import calcLatLong as cll
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import cProfile
import calcLatLong
from math import radians, cos, sin, asin, sqrt

class MyStuff(object):

	def __init__(self):
		self.datetimelist = [(datetime.datetime(2000,1,1,0,0,0,0),datetime.datetime(2000,1,1,5,0,0,0)),
		(datetime.datetime(2000,1,2,10,0,0,0),datetime.datetime(2000,1,2,15,0,0,0)),
		(datetime.datetime(2000,1,3,20,0,0,0),datetime.datetime(2000,1,3,23,0,0,0)),
		(datetime.datetime(2000,1,4,10,0,0,0),datetime.datetime(2000,1,4,15,0,0,0)),
		(datetime.datetime(2000,1,5,0,0,0,0),datetime.datetime(2000,1,5,15,0,0,0))		
		]

		self.integers = []

	def calcDistances(self):
		
		haversine(42,-71,thing1,thing2)

	def haversine(self, lon1, lat1, lon2, lat2):
	    """
	    Calculate the great circle distance between two points 
	    on the earth (specified in decimal degrees)
	    """
	    # convert decimal degrees to radians 
	    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

	    # haversine formula 
	    dlon = lon2 - lon1 
	    dlat = lat2 - lat1 
	    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	    c = 2 * asin(sqrt(a)) 

	    # 6367 km is the radius of the Earth
	    km = 6367 * c
	    return km

	def makeLocation(self, latlon=(42.3417,70.9661)):
		self.latlon = latlon

	def datespan(self):
		"create a list of date objects that iterate through a start and end date"
		self.things=[]

		def tmpdatespan(startDate, endDate, delta=timedelta(days=1)):
		    currentDate = startDate
		    while currentDate < endDate:
		        yield currentDate
			currentDate += delta

		for day in tmpdatespan(date(2007, 1, 1), date(2008, 1, 1), delta=timedelta(days=1)):
			self.things.append(day)

		print self.things

		return self.things

	def calcR(self, lat, lon, dates):
		self.datetimelist=[]
		for day in dates:
			risesettime = calcLatLong.calcRiseSet(lat,lon,day)
			self.datetimelist.append(risesettime)
		print self.datetimelist


	def profile(self):
		cProfile.runctx('self.fixedsunset(5,15)',globals(),locals())

	def parseList(self):
		sunrise=[]
		sunset=[]
		for x in self.datetimelist:
			sunrise.append(x[0])
			sunset.append(x[1])
		print [sunrise,sunset]
		return [sunrise,sunset]

	def getIntegers(self):
			return self.integers

	def takeSTD(self,listofthings):
			return np.std(listofthings)

	def addErrors(self,datetime,number,length):
		#returns list of datetimes with error added to them
		#there are number amounts of these datetimes
		#the datetimes are within 'length' of the estimated given datetime
		self.addedErrors = []
		integers = []

		for i in range(number):
			integer = random.randint(-length,length)
			d=timedelta(minutes=integer)
			error = datetime + d
			self.addedErrors.append(error)
			integers.append(integer)
		return self.addedErrors, integers, datetime

	# def fixedsunrise(self,number,length, approx=(42,-71)):
	# 	self.latlonlist =[]
	# 	#a list of fixed sunrises
	# 	#added errors of the sunset times
	# 	listoftimes=parseList(times)
	# 	for risetime,settime in self.datetimelist:
	# 		[settimes,integers]=self.addErrors(settime,number,length)
	# 		for errorsettime in settimes:
	# 			latlon = cll.calcLatLon(risetime,errorsettime,approx)
	# 			self.latlonlist.append(latlon)
	# 			print risetime.date()
	# 			print latlon
	# 	print 'a'
	# 	print self.latlonlist
	# 	print 'b'
	# 	return self.latlonlist

	def fixedsunset(self,number,length, approx=(42,-71)):

		self.datelatlonlist=[]
	#	self.integerlist = []

		#a list of fixed sunsets
		#added errors of the sunrise times 
		#listoftimes=self.parseList(times)
		for risetime,settime in self.datetimelist:
			[risetimes,integers,datetime]=self.addErrors(risetime,number,length)

			self.latlonlist=[]
			for errorrisetime in risetimes:
				latlon = cll.calcLatLon(errorrisetime,settime,approx)
				#print latlon
				self.latlonlist.append(latlon)
			self.datelatlonlist.append([settime.date(),self.latlonlist,integers])

			print self.datelatlonlist

		print self.datelatlonlist

		return self.latlonlist #this should be erased

	def dictParse(self):

		self.lats = []
		self.lons = []
		self.dates = []

		for k,v,y in self.datelatlonlist: #date,(lon,lat),error
			londate = []
			latdate = []
			for i in range(len(v)):
				londate.append(v[i][0]) #lon
				latdate.append(v[i][1]) #lat
			lonstd = np.std(londate)
			latstd =  np.std(latdate)
			gsstd= np.std(y)
			self.dates.append(k)
			self.lons.append(lonstd/gsstd)
			self.lats.append(latstd/gsstd)

		plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
		plt.gca().xaxis.set_major_locator(mdates.DayLocator())
		g1, = plt.plot(self.dates,self.lats)
		g2, = plt.plot(self.dates,self.lons)
		plt.xlabel('Date')
		plt.ylabel('STD/Gaussian STD')
		plt.gcf().autofmt_xdate()
		plt.legend([g1, g2], ["lat", "lon"])
		plt.show()


	def notfixed():
		#skip for now
		pass

	def lookatLat(self,listoflatlons):
		lats = []
		for latlon in listoflatlons:
			lats.append(latlon[0])
		return lats

	def lookatLon(self,listoflatlons):
		lons = []
		for latlon in listoflatlons:
			lons.append(latlon[1]) 
		return lons	

def main():
	
	hello = MyStuff()
	#hello.profile()
	dates = hello.datespan()
	hello.calcR(42.358,-71.064,dates)
	hello.fixedsunset(10,5)
	#hello.fixedsunset(5,5)
	hello.dictParse()

if __name__ == '__main__':
	main()