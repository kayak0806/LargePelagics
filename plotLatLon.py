import Pysolar
import datetime
import math
import thinkplot



dateCurrent = datetime.datetime.utcnow() # create a datetime object for now
altCurrent = Pysolar.GetAltitude(42.293247,-71.263633,dateCurrent)
azmCurrent = Pysolar.GetAzimuth(42.293247,-71.263633,dateCurrent)
datenoon =  dateCurrent.replace(hour = 12, minute = 0,second=0,microsecond=0)
altNoon = Pysolar.GetAltitude(42.293247,-71.263633,dateCurrent)
posNE = (42.293247,-71.263633)

def getLat(lon, day, altGoal):

	for lat in range(-90,90):
		print Pysolar.GetAltitude(lat,lon,day)

	return lat

timeRise = datetime.time(10,22)
timeSet = datetime.time(21,34)

sunrise = datetime.datetime.combine(dateCurrent.date(),timeRise)
sunset  = datetime.datetime.combine(dateCurrent.date(),timeSet)

print Pysolar.GetAltitude(posNE[0],posNE[1],sunrise)
print Pysolar.GetAltitude(posNE[0],posNE[1],sunset)

# Sweep over all lat/long
def fullSweep():
	longRange = [i-180 for i in range(360+1)]
	latRange = [i-90 for i in range(180+1)]

	match = []
	Rise = []
	Set = []

	for lat in latRange:
		for lon in longRange:
			matchRise = math.floor(Pysolar.GetAltitude(lat,lon,sunrise))==0
			matchSet  = math.floor(Pysolar.GetAltitude(lat,lon,sunset))==0
			if (matchRise and matchSet):
				match.append( (lat,lon) )
			if (matchRise):
				Rise.append((lat,lon))
			if (matchSet):
				Set.append((lat,lon))


	print match
	latAlt,lonAlt = zip(*match)
	# latAzm,lonAzm = zip(*Set)
	thinkplot.Scatter(lonAlt,latAlt)
	# thinkplot.Scatter(lonAzm,latAzm)
	thinkplot.Show()

# fullSweep()