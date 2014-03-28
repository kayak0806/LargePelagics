import datetime
import random
import scipy.stats as stats
import thinkplot as tp
import calcLatLong as cll

testdatetime=datetime.datetime(2000,1,1,0,0,0,0)

#test sunrise,sunset

datetimelist = [(datetime.datetime(2000,1,1,0,0,0,0),datetime.datetime(2000,1,1,5,0,0,0)),(datetime.datetime(2000,1,1,10,0,0,0),datetime.datetime(2000,1,1,15,0,0,0))]

def parseList(datetimelist):
	for x in datetimelist:
		sunrise = x[0]
		sunset = x[1]
		print sunrise
		print sunset

#end test times

#add errors here
def addErrors(number,length):
	#returns list of datetimes with error added to them
	#there are number amounts of these datetimes
	#the datetimes are within 'length' of the estimated given datetime
	addedErrors = []
	for i in range(number):
		integer = random.randint(-length,length)
		d=datetime.timedelta(minutes=integer)
		error = testdatetime + d
		addedErrors.append(error)
	return addedErrors

def fixedsunrise(number,length,risetime,approx=(42,-71)):
	#a list of fixed sunrises
	#added errors of the sunset times
	risetime = risetime.time()
	settimes=addErrors(number,length)
	print 'a'
	for settime in settimes:
		print 'b'
		day = settime.date()
		settime = settime.time()
		print 'c'
		latton = cll.calcLatLon(risetime,settime,day,approx)
		print 'd'

		print latton


	# call calculation thing


def fixedsunset():
	#a list of fixed sunsets
	#added errors of the sunrise times
	pass

def notfixed():
	#everything is not fixed
	pass

#for loop end


#def 

#def p value


#def error plot
	#a sequence of p value out/p value in over time.
	#random data (buzz, buzz)
	#the p value is __ 
	#error thing from the error from approx
	#error thing from the guess
	#error thing over error from approx

#def input integers
	#normalize

#print 

#def random_number_generator():

	#datetime.datetime()

def main():
	fixedsunrise(5,15,testdatetime)
	print 'hello'
	#addErrors(5,15)

if '__name__' == main():
	main()