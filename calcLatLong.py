import Pysolar
import datetime
import math
import thinkplot



def calcLatLon(riseDate,setDate, approx=(42,-71)):
	# riseDate: datetime when rising sun is at horizon
	# setDate: datetime when setting sun is at horizon
	# day: date of measurment
	# approx: approximate known posion ()
	# returns: matchimg position on same side of earth as approx

	longRange = [i-180 for i in range(360+1)]
	latRange = [i-90 for i in range(180+1)]

	# riseDate = datetime.datetime.combine(day,riseTime)
	# setDate = datetime.datetime.combine(day,setTime)

	matches = []

	for lat in latRange:
		for lon in longRange:
			riseAlt = Pysolar.GetAltitude(lat,lon,riseDate)
			setAlt = Pysolar.GetAltitude(lat,lon,setDate)
			matchRise = math.floor(riseAlt)==0
			matchSet  = math.floor(setAlt)==0
			if (matchRise and matchSet):
				matches.append( (lat,lon) )

	twoMatches = splitMatches(matches)
	return closestMatch(twoMatches,approx)



def splitMatches(matches):
	# There will always be two match ponts directly across from each other
	# Take the rough matches, split by which side they're on
	# average and return both exact matches

	# get average
	X,Y = zip(*matches)
	aveX = sum(X)/len(X)
	# split matches
	matchA = []
	matchB = []
	for p in matches:
		x,y = p
		if (x<aveX):
			matchA.append((x,y))
		else:
			matchB.append((x,y))
	# average positions
	xA,yA=zip(*matchA)
	xA = sum(xA)/len(xA)
	yA = sum(yA)/len(yA)
	xB,yB=zip(*matchB)
	xB = sum(xB)/len(xB)
	yB = sum(yB)/len(yB)

	return [(xA,yA),(xB,yB)]

def closestMatch(matches, guess):
	# The two matches will always be directly across from each other
	# The guess just has to be in the right hemisphere
	xA,yA = matches[0]
	xB,yB = matches[1]

	distA = ((guess[0]-xA)**2 + (guess[1]-yA)**2)**.5
	distB = ((guess[0]-xB)**2 + (guess[1]-yB)**2)**.5
	
	if (distA<distB):
		return (xA,yA)
	else:
		return (xB,yB)


