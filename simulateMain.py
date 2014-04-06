import datetime
import sunloc
import numpy
import thinkplot
import introduceError
import matplotlib.pyplot as plt
import scipy.stats
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
endDate = datetime.date(2014,1,31) # dec 31, 2014
lat,lon = (42.291625,-71.264406)    # Olin College

# generate days
def dateSpan(startDate, endDate, delta=datetime.timedelta(days=1)):
    '''creates a list of date objects between a start and end date'''
    dates = []
    currentDate = startDate
    while currentDate < endDate:
        currentDate += delta
        dates.append(currentDate)
    return dates

dates = dateSpan(startDate,endDate,datetime.timedelta(days=1)) # increment by 1 week

# get rise/set times
riseSet = []
for day in dates:
    riseSet.append(sunloc.calcRiseSet(lat,lon,day))

# introduce error
sigma = 5 # 95% of errors will be +/- 10 minutes
size = 5 # generate 100 values
errorsLat = []
errorsLon = []

for day in riseSet:
    error = introduceError.introduceError(0,sigma,size,day)
    errorsLat.append(error[0]) # add error stuff
    errorsLon.append(error[1])


# calculate location
print 'location'
print len(errorsLat)
def allLocations(day):
    '''calculates the location for each (rise,set) datetime in array'''
    loc = []
    for risedate,setdate in day:
        loc.append(sunloc.calcLatLon(risedate,setdate))
    return loc

locations = []
for day in errorsLat:
    locations.append(allLocations(day))

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*numpy.array(data)
    n = len(a)
    m, se = numpy.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h

# find accuracy
print 'accuracy'
def accuracy(locations, start):
    lat,lon = start
    lats,lons = zip(*locations)
    dlat = [l-lat for l in lats]
    dlon = [l-lon for l in lons]
    latinfo = mean_confidence_interval(dlat)
    loninfo = mean_confidence_interval(dlon)

    #meanLat = numpy.mean(dlat)
    #meanLon = numpy.mean(dlon)
    #return (meanLat, meanLon)
    return latinfo,loninfo
latinfos = []
loninfos= []
for day in locations:
    latinfo,loninfo=accuracy(day,(lat,lon))
    latinfos.append(latinfo)
    loninfos.append(loninfo)

print 'averages'

#means,uppers,lowers = zip(*latinfos)
means,uppers,lowers = zip(*loninfos)

# plot accuracy

#print len(averages), len(dates)
#aveLat,aveLon = zip(*averages)


#thinkplot.Scatter(dates,aveLat)

plt.plot(dates,means)
plt.plot(dates,uppers)
plt.plot(dates,lowers)
plt.show()
#thinkplot.Scatter(dates,aveLon)
#thinkplot.Show()