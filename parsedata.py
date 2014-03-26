"""parsedata.py"""

"""Reads drifter.tab and returns an array of datapoints. 
Each datapoint is an array of datetime, depth, light, temeperature."""


import datetime
import argparse

def openFile(fname,flag='r'):  

  fin = open(fname,flag)

  return fin

def parseFile(fname):
	fin = openFile(fname)
	fin.readline()
	points = []
	for line in fin:
	  #line: year, month, day, hour, minute, second, light, depth, temp
		line = line.split(" ")
		for i in range(6):
			line[i]=int(line[i])
		for i in range(3):
			line[i+6]=float(line[i+6])
		date = datetime.datetime(line[0],line[1],line[2],line[3],line[4],line[5])
		point = [date,line[6],line[7],line[8]]
		points.append(point)
	fin.close()
	return points


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('input')
  args = parser.parse_args()

  fname = args.input
  out = parseFile(fname)
  print out

  
  #print parseFile('drifter.tab')

if __name__ == "__main__":
	main()
	
	
	
	
