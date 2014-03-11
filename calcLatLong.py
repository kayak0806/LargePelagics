import Pysolar
import datetime
import math
import thinkplot



def calcLatLon(riseDate,setDate, approx=(42,-71)):
	# riseDate: datetime when rising sun is at horizon
	# setDate: datetime when setting sun is at horizon
	# approx: approximate known posion ()
	# returns: matchimg position

	altRise = Pysolar.GetAltitude(approx[0],approx[1], riseDate)
	altSet = Pysolar.GetAltitude(approx[0],approx[1], setDate)
	dist = ( altRise**2 + altSet**2 )**0.5
	current = (dist,approx)
	while (math.floor(current[0])!=0):
		latCur,lonCur = current[1]
		next = [
			(latCur+1,lonCur),
			(latCur,lonCur+1),
			(latCur-1,lonCur),
			(latCur,lonCur-1)
			]
		nextVal = []
		for lat,lon in next:
			altRise = Pysolar.GetAltitude(lat,lon, riseDate)
			altSet = Pysolar.GetAltitude(lat,lon, setDate)
			dist = ( altRise**2 + altSet**2 )**0.5
			nextVal.append((dist,(lat,lon)))
		current = min(nextVal)
	return current[1]


