import parsedata
import getRiseSet
import datetime


# reads the mooring.tab file
# formats it
# saves it to mooring.txt

def daystr(dt):
	# format: year month day hour minute
	format = "%y %m %d %H %M"
	return dt.strftime(format)

def destring(str):
	format = "%y %m %d %H %M"
	return datetime.datetime.strptime(str,format)

data = parsedata.parseFile('mooring.tab')
fdata = getRiseSet.allRiseSet(data)
fout = open('mooring.txt','w')


for day in fdata:
	line = daystr(day[0])+", "+daystr(day[1])+"\n"
	fout.write(line)

print 'done'