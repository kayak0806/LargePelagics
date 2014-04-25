import datetime
import sunloc
import numpy
import thinkplot
import introduceError
import matplotlib.pyplot as plt
import scipy.stats
import cProfile
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
sigma = 5 
size = 5 
errorsLat = []
errorsLon = []

for day in riseSet:
    error = introduceError.introduceError(0,sigma,size,day)
    errorsLat.append(error[0]) # add error stuff
    errorsLon.append(error[1])

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

def accuracy(locations, start):
    lat,lon = start
    lats,lons = zip(*locations)
    dlat = [l-lat for l in lats]
    dlon = [l-lon for l in lons]
    latinfo = mean_confidence_interval(dlat)
    loninfo = mean_confidence_interval(dlon)
    return latinfo,loninfo

latinfos = []
loninfos= []


for day in locations:
    latinfo,loninfo=accuracy(day,(lat,lon))
    latinfos.append(latinfo)
    loninfos.append(loninfo)

def timeConversion(a):
    #defunct
    pass

    # for info in a:
    #     for thing in info[0]:
    #         lat=thing[0]
    #         lon=thing[1]
    #         times.append(sunloc.calcRiseSet(lat,lon,info[1]))
    # print times
    # sunloc.calcRiseSet(info)

means,uppers,lowers = zip(*latinfos)
#means,uppers,lowers = zip(*loninfos)

print means

def calculateDays(averages):
#calculate dates the months where function is most accurate 

    a = [ i for i in range(len(averages)) if abs(averages[i])<1]
    print a

    b = [ dates[a[i]] for i in range(len(a))]
    print b

#calculateDays(means)

def plotAccuracy(averages,ups,downs):
#plots the summary analysis graph
    from matplotlib.dates import HourLocator, DayLocator, DateFormatter

    plt.plot(dates,averages)
    plt.plot(dates,ups)
    plt.plot(dates,downs)
    days = DayLocator(interval=1)
    hours = HourLocator(interval=6)
    daysFmt = DateFormatter('%d')
    plt.gca().xaxis.set_major_locator(days)
    plt.gca().xaxis.set_major_formatter(daysFmt)
    plt.gca().xaxis.set_minor_locator(hours)
    plt.xticks(rotation=30,ha='right')
    plt.show()

plotAccuracy(means,uppers,lowers)
