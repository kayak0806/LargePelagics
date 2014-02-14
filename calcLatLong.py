import Pysolar
import datetime

d = datetime.datetime.utcnow() # create a datetime object for now


lat = 0
lon = -71.2450
alt = Pysolar.GetAltitude(lat,lon,d)

while alt >=Pysolar.GetAltitude(42.2793, -71.2450, d):

	lat += 1
	alt = Pysolar.GetAltitude(lat,lon,d)

print 'alt, lat'
print Pysolar.GetAltitude(lat,lon,d), lat

	
lat = 90
lon = -71.2450
alt = Pysolar.GetAltitude(lat,lon,d)

while alt <=Pysolar.GetAltitude(42.2793, -71.2450, d):
	lat -= 1
	alt = Pysolar.GetAltitude(lat,lon,d)
print Pysolar.GetAltitude(lat,lon,d), lat