import Pysolar
from Pysolar import util
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

def calcLatLon2(riseDate,setDate, approx=(42,-71)):
	# riseDate: datetime when rising sun is at horizon
	# setDate: datetime when setting sun is at horizon
	# approx: approximate known posion ()
	# returns: matchimg position
	date = riseDate.date()

	riseApprox,setApprox = calcRiseSet(approx[0],approx[1],date)
	dist = ( (riseDate-riseApprox).total_seconds()**2 + (setDate-setApprox).total_seconds()**2 )**0.5
	current = (dist,approx)
	next=[]

	# while (current[0] >= 0):
	for i in range(10):
		print current[0]
		latCur,lonCur = current[1]
		next = [
			(latCur+10,lonCur),
			(latCur,lonCur+10),
			(latCur-10,lonCur),
			(latCur,lonCur-10)
			]
		nextVal = []
		for lat,lon in next:
			print lat,lon
			riseCur,setCur = calcRiseSet(lat,lat,date)
			risedist = (riseDate-riseCur).total_seconds()
			setdist = (setDate-setCur).total_seconds()
			dist = ( risedist**2 + setdist**2 )**0.5
			nextVal.append( (dist,(lat,lon)) )
		current = min(nextVal)
	return current[1]

def calcRiseSet(lat,lon,date):
	# takes a lat, lon, and datetime.date object
	# returns sunset and sunrise in UTC as datetime.datetime object
	d = datetime.datetime.combine(date,datetime.time(hour=0))
	d.replace(tzinfo = UTC())
	sunrise,sunset =  Pysolar.util.GetSunriseSunset(lat,lon,d,0)
	return (sunrise, sunset)



class UTC(datetime.tzinfo):
	def utcoffset(self,dt):
		return datetime.timedelta(hours=0)
	def dst(self,dt):
		return datetime.timedelta(hours=0)
	def tzname(self,dt):
		return "UTC"
