#dates where least measurement error
#of those dates, run the sun loc and lat;
#this is now our sun loc and lat

#populate a list
#1-60,#182-244,#305-364

# jan 1 - mar 1
# jul 1 - sep 1
# nov 1 - dec 31

import timeit

import sunloc
from readData import readFile

a=readFile('mooring.txt')

dates_index=range(1,60) + range(182,244) + range(305,364)

dates_index = []
latlons = []

for i in range(len(a)):
	if a[i][0].month == 1 or 2 or 7 or 8 or 11 or 12:
		dates_index.append(i)
print dates_index
# print len(dates_index)
for i in range(len(dates_index)):

	#print a[dates_index[i]]
	latlons.append(sunloc.calcLatLon(a[dates_index[i]][0],a[dates_index[i]][1]))

	print i

print latlons


