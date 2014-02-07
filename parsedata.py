"""parsedata.py"""

"""Reads drifter.tab and returns an array of datapoints. 
Each datapoint is an array of datetime, light, depth, temeperature."""


import datetime
import argparse

def openFile(fname):
  

  fin = open(fname)

  return fin

def parseFile(fname):
	fin = openFile(fname)
	print 'merp'
	fin.readline()
	points = []
	for line in fin:
	  #line: year, month, day, hour, minute, second, light, depth, temp
		line = line.split(" ")
		line = [int(i) for i in line]
		date = datetime.datetime(line[0],line[1],line[2],line[3],line[4],line[5])
		point = [date,line[6],line[7],line[8]]
		points.append(point)
	return points
	

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('name')
  args = parser.parse_args()

  fname = args.name
  print parseFile(fname)
  
  
  #print parseFile('drifter.tab')

if __name__ == "__main__":
	main()
	
	
	
	
