import datetime




def readFile(filename):
	fin = open(filename,'r')
	data = []
	for line in fin:
		line = line.split(", ")
		sunrise = destring(line[0])
		sunset = destring(line[1].rstrip())
		data.append((sunrise,sunset))
	return data





# Helper functionis
def destring(str):
	format = "%y %m %d %H %M"
	return datetime.datetime.strptime(str,format)

if __name__=="__main__":
	data = readFile('mooring.txt')
	print data