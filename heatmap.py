import Pysolar
from Pysolar import util
import datetime
import math
import numpy
from matplotlib import pyplot as plt
from scipy.stats import norm
import sunloc
import readData

class World(object):
		def __init__(self,scale):
			self.scale = scale
			self.values = dict()
			latRange,lonRange = (-89,89),(-179,179)
			self.lats = range(latRange[0],latRange[1],scale #[latRange[0]+scale*i  for i in range(int((latRange[1]-latRange[0])/scale))]
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

def riseProb(lat,lon, date, delta):
  # for now, the prob is the same for every location and date
  
  p = norm(loc=0,scale=5*60)
  #loc = mean, scale=std in seconds
  return p.pdf(delta)
def setProb(lat,lon,date,delta):
  # for now, same as rise
  return riseProb(lat,lon,date,delta)
 
def mapProb(riseDate,setDate):
  today = riseDate.date()
  world = World(1)
  #today = datetime.date.today()
  # riseTime = datetime.time(10,2)
  # setTime = datetime.time(23,26)
  # riseDate = datetime.datetime.combine(today,riseTime)
  # setDate = datetime.datetime.combine(today,setTime)
  # lat,lon = 42,-71.264406
  # riseDate,setDate = sunloc.calcRiseSet(0,0,today)
  
  for pos in world.allPos():
    lat,lon = pos
    rDate,sDate = sunloc.calcRiseSet(lat,lon,today)
    rDif = (rDate - riseDate).total_seconds()
    sDif = (sDate - setDate).total_seconds()
    prob = riseProb(lat,lon,today,rDif)*setProb(lat,lon,today,sDif)
    world.write(pos,prob)
    
  return world
def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

def maxProb(world):
	d = world.values
	return keywithmaxval(d)

def posOut():
	fin = open("mooringLocations.txt",'r')
	posout = []
	for l in fin:
		pos = l.split(" ")
		print pos
		posout.append(pos)
	return posout

mooring = readData.readFile("mooring.txt")
fint = open("mooringLocations.txt",'r')
fout = open("mooringLocDate.txt",'w')
points = len(mooring)
for i in range(points):
	day = mooring[i]
	probMap = mapProb(day[0],day[1])
	prob = maxProb(probMap)
	fout.write(str(prob[0])+" "+str(prob[1])+"\n")
	# check = sunloc.calcRiseSet(-37,-14,day[0].date())
	# print "given times: ",day`2`2``
	# print "calc  times: ",check
	# tmr = day[0].time().hour*60+(day[0].time().minute)
	# tms = day[1].time().hour*60+(day[1].time().minute)
	plt.plot(day[0].date(),prob[0],'ro')
	print i
fout.close()
print "ploting"
# plt.axis([-180,180,-90,90])
plt.show()


# prob2 = mapProb(mooring[50][0],mooring[50][1])
# print maxProb(prob1)
# prob2 = mapProb(mooring[1][0],mooring[1][1])
# plt.figure(1)
# plt.pcolor(prob1.toArray())
# plt.figure(1)
# plt.pcolor(prob2.toArray())
# plt.show()
