"""parsedata.py"""

"""Reads drifter.tab and returns an array of datapoints. 
Each datapoint is an array of datetime, light, depth, temeperature."""


import datetime

def main():
	f = open('drifter.tab')
	f.readline()
	points = []
	for line in f:
		line = line.split(" ")
		line = [int(i) for i in line]
		date = datetime.datetime(line[0],line[1],line[2],line[3],line[4],line[5])
		point = [date,line[6],line[7],line[8]]
		points.append(point)
	return points

if __name__ == "__main__":
	main()