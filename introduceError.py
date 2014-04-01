#input 3 things
#mu, mean, sunrise,sunset datetime
#output two lists of changed sunrise, sunset datetime, sunrise, changed sunset datetime

import random
from datetime import timedelta, datetime, date
import datetime

def rError(mu,mean,datetime):

	integer = random.gauss(mu,mean)
	d = timedelta(minutes=integer)*10
	r = (d + datetime[0],datetime[1])

	return r

def sError(mu,mean,datetime):

	integer = random.gauss(mu,mean)
	d = timedelta(minutes=integer)*10
	s = (datetime[0],d + datetime[1])

	return s

def introduceError(mu,mean,number,datetime):
	rs = []
	ss = []
	for blah in range(number):
		r = rError(mu,mean,datetime)
		s = sError(mu,mean,datetime)
		rs.append(r)
		ss.append(s)
	return rs, ss

def main():
	introduceError(0,1,10,(datetime.datetime(2000,1,1,0,0,0,0),datetime.datetime(2000,1,1,5,0,0,0)))


if __name__ == '__main__':
	main()
