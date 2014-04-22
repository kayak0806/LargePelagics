import Pysolar
from Pysolar import util
import datetime
import math
import numpy
from matplotlib import pyplot as plt

'''calcLatLon gets rise/set from lat/lon
	calcRiseSet gets lat/lon from rise/set'''

def calcLatLon(riseDate,setDate, approx=(30,-60)):
	# riseDate: datetime when rising sun is at horizon
	# setDate: datetime when setting sun is at horizon
	# approx: approximate known posion ()
	# returns: matchimg position

	altRise = Pysolar.GetAltitude(approx[0],approx[1], riseDate)
	altSet = Pysolar.GetAltitude(approx[0],approx[1], setDate)
	dist = ( altRise**2 + altSet**2 )**0.5
	current = (dist,approx)
	i=0
	while (math.floor(current[0]*10.0)/10>=1):
		i+=1
		# print current
		latCur,lonCur = current[1]
		next = [
			(latCur+.1,lonCur),
			(latCur,lonCur+.1),
			(latCur-.1,lonCur),
			(latCur,lonCur-.1)
			]
		nextVal = []
		for lat,lon in next:
			altRise = Pysolar.GetAltitude(lat,lon, riseDate)
			altSet = Pysolar.GetAltitude(lat,lon, setDate)
			dist = ( altRise**2 + altSet**2 )**0.5
			nextVal.append((dist,(lat,lon)))
		current = min(nextVal)
	return current[1]

def calcLatLon2(riseDate,setDate, approx=(20,-50)):
	# NOT WORKING YET
	# riseDate: datetime when rising sun is at horizon
	# setDate: datetime when setting sun is at horizon
	# approx: approximate known posion ()
	# returns: matchimg position
	date = riseDate.date()

	def search(val):
		dist, guess,path = val
		print dist
		if dist<10:
			print dist
			return guess
		
		glat,glon = guess
		next = [
			(glat-.1,glon),
			(glat,glon-.5),
			(glat+.1,glon),
			(glat,glon+.5)
			]
		vals = []
		
		for n in next:
			if n not in path:
				nrise,nset = calcRiseSet(n[0],n[1],date)
				risedist = (riseDate-nrise).total_seconds()
				setdist = (setDate-nset).total_seconds()
				newdist = ( (risedist)**2 + (setdist)**2)**.5
				newpath = path+[n]
				vals.append((newdist,n,newpath))
		if not vals:
			# for p in path[100::]:
				# print p
			return guess
		return search(min(vals))

	grise,gset = calcRiseSet(approx[0],approx[1],date)
	risedist = (riseDate-grise).total_seconds()
	setdist = (setDate-gset).total_seconds()
	dist = ( (risedist)**2 + (setdist)**2)**.5			

	return search( (dist,approx,[]) )




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

def main():
	# for every possible latitude (-90 to 90)
	# and every possible longitude (-180 to 180)
	# at some scale (ie 1degree, 0.1degree, etc)
	# calculate the "distance" between the rise-set time
	# at that position and the actual rise-set time
	# plot those values

	class World(object):
		def __init__(self,scale):
			self.scale = scale
			self.values = dict()
			latRange,lonRange = (-90,90),(-180,180)
			self.lats = [latRange[0]+scale*i  for i in range(int((latRange[1]-latRange[0])/scale))]
			self.lons = [lonRange[0]+scale*i  for i in range(int((lonRange[1]-lonRange[0])/scale))]
			for lat in self.lats:
				for lon in self.lons:
					self.values[(lat,lon)]=0

		def allPos(self):
			return self.values.keys()

		def value(self,pos):
			if pos in self.values:
				return self.values[pos]
			else:
				print "not a valid location\n"
				return 0
		def write(self,	pos,value):
			if pos in self.values:
				self.values[pos]=value
				return 1
			else:
				print "not a valid location\n"
				return 0
		def toArray(self):
			a = len(self.lats)
			b = len(self.lons)
			matrix = [[i for i in range(b)] for j in range(a)]
			for x in range(a):
				for y in range(b):
					lat,lon = self.lats[x],self.lons[y]
					val = self.value((lat,lon))
					matrix[x][y] = val
			return numpy.array(matrix)

	world = World(1)
	today = datetime.date.today()
	# riseTime = datetime.time(10,2)
	# setTime = datetime.time(23,26)
	# riseDate = datetime.datetime.combine(today,riseTime)
	# setDate = datetime.datetime.combine(today,setTime)
	lat,lon = 42,-71.264406
	riseDate,setDate = calcRiseSet(0,0,today)

	for pos in world.allPos():
		lat,lon = pos
		# Calculate 'cost'
		# riseCur,setCur = calcRiseSet(lat,lon,today)
		# risedist = (riseDate-riseCur).total_seconds()
		# setdist = (setDate-setCur).total_seconds()
		# dist = ( (risedist)**2 + (setdist)**2)**.5
		altRise = Pysolar.GetAltitude(lat,lon, riseDate)
		altSet = Pysolar.GetAltitude(lat,lon, setDate)
		dist = ( altRise**2 + altSet**2 )**0.5
		if dist==0:
			print pos, dist
		world.write(pos,dist)
	print len(world.allPos())

	plt.pcolor(world.toArray())	
	plt.show()
		



if __name__ == '__main__':
	main()