import readData
import formatMooring
import datetime
import sunloc
from matplotlib import pyplot as plt

def posOut():
	fin = open("mooringLocDate.txt",'r')
	posout = []
	for l in fin:
		line = l.split(",")
		day = (formatMooring.destring(line[0]),formatMooring.destring(line[1]))
		pos = tuple([int(l.strip("\n")) for l in line[2].split(" ")])
		posout.append([day,pos])
	fin.close()
	return posout

data = posOut();

for day,loc in data:
	date = day[0].date()
	print date
	crise,cset = sunloc.calcRiseSet(loc[0],loc[1],date)
	dif = (day[1]-day[0]).total_seconds()
	difc = (cset-crise).total_seconds()
	plt.plot(date,loc[0],"ro")
	# plt.plot(date,difc/3600.0,"bo")
	# plt.plot(date,cset.minute,"bo")
# plt.axis([-180,180,-90,90])
plt.show()

# mooring = readData.readFile("mooring.txt")
# fin = open("mooringLocations.txt",'r')
# fout = open("mooringLocDate.txt",'w')
# i = 0
# for l in fin:
# 	ml = mooring[i]
# 	day = formatMooring.daystr(ml[0])+","+formatMooring.daystr(ml[1])
# 	line = day+","+l
# 	fout.write(line)
# 	print line.split(",")
# 	i+=1
	