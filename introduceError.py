#input 3 things
#mu, sigma, sunrise,sunset datetime
#output two lists of changed sunrise, sunset datetime, sunrise, changed sunset datetime

import random
from datetime import timedelta, datetime, date
import datetime

def rError(mu,sigma,datetimes):

	integer = random.gauss(mu,sigma)
	d = timedelta(minutes=integer)
	r = (d + datetimes[0],datetimes[1])

	return r

def sError(mu,sigma,datetimes):

	integer = random.gauss(mu,sigma)
	d = timedelta(minutes=integer)
	s = (datetimes[0],d + datetimes[1])

	return s

def introduceError(mu,sigma,number,datetimes):
	rs = []
	ss = []
	for i in range(number):
		r = rError(mu,sigma,datetimes)
		s = sError(mu,sigma,datetimes)
		rs.append(r)
		ss.append(s)
	return rs, ss

def main():
	introduceError(0,1,10,(datetime.datetime(2000,1,1,0,0,0,0),datetime.datetime(2000,1,1,5,0,0,0)))


if __name__ == '__main__':
	main()
