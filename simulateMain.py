import datetime
import sunloc
# import (error stuff)
'''
plan for main:
	generate list of days
	get list of rise/set times for those days
	introduce errors for each time
	calculate location for each rise/set times
	calculate accuracy
	plot accuracy
'''
# general parameters:
startDate = datetime.date(2014,1,1) # jan 01, 2014
endDate = datetime.date(2014,12,31) # dec 31, 2014
lat,lon = (42.291625,-71.264406)	# Olin College

# generate days
dates = dateSpan(startDate,endDate,days=7) # increment by 1 week

def dateSpan(startDate, endDate, delta=timedelta(days=1)):
'''creates a list of date objects between a start and end date'''
	dates = []
    currentDate = startDate
    while currentDate < endDate:
		currentDate += delta
		dates.append(currentDate)
	return dates

# get rise/set times
riseSet = []
for day in dates:
	riseSet.append(sunloc.getRiseSet(lat,lon,day))

# introduce error
sigma = 5 # 95% of errors will be +/- 10 minutes
size = 25 # generate 100 values
errors = []

for day in riseSet:
	errors.append([day]) # add error stuff


# calculate location
locations = []
for day in errors:
	locations.append(allLocations(day))

def allLocations(day):
	'''calculates the location for each (rise,set) datetime in array'''
	loc = []
	for risedate,setdate in day:
		loc.append(sunloc.calcLatLon(risedate,setdate))
	return loc

# find accuracy

# plot accuracy






