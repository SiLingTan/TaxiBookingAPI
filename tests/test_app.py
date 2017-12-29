
"""
Name: Tan Si Ling
Date Implemented : 28th December 2017

Program: Taxi Booking System
Description: Unit Tests for Taxi Booking Application

"""

#!flask/bin/python
from app import *

def test_increment_system_time():
	assert incrementSystemTime() == 1


def test_reset_function():
	assert resetTaxiSystem() == 0

	assert cars[0]['x'] == 0
	assert cars[0]['y'] == 0
	assert cars[0]['booked'] == False
	assert cars[1]['x'] == 0
	assert cars[1]['y'] == 0
	assert cars[1]['booked'] == False
	assert cars[2]['x'] == 0
	assert cars[2]['y'] == 0
	assert cars[2]['booked'] == False

def prepCars():

	# car id 1,3 is are not booked and at the same location
	# car id 1 should be used first
	testCars1 = [
		{
			'id': 1,
			'x': 1000,
			'y': 0,
			'booked': False,
			'bookedTillTime': -1
		},
		{
			'id': 2,
			'x': 10,
			'y': 0,
			'booked': True,
			'bookedTillTime': 100
		},
		{
			'id': 3,
			'x': 1000,
			'y': 0,
			'booked': False,
			'bookedTillTime': -1
		}
	]


	testCars2 = [
		{
			'id': 1,
			'x': 10,
			'y': 10,
			'booked': False,
			'bookedTillTime': -1
		},
		{
			'id': 2,
			'x': -60,
			'y': -60,
			'booked': False,
			'bookedTillTime': -1
		},
		{
			'id': 3,
			'x': 30,
			'y': -10,
			'booked': False,
			'bookedTillTime': -1
		}
	]

	#swap id 1 and 3 from testCar2 to ensure 
	#that distance followed by id would always be picked up first
	testCars3 = [
		{
			'id': 3,
			'x': 10,
			'y': 10,
			'booked': False,
			'bookedTillTime': -1
		},
		{
			'id': 2,
			'x': -60,
			'y': -60,
			'booked': False,
			'bookedTillTime': -1
		},
		{
			'id': 1,
			'x': 30,
			'y': -10,
			'booked': False,
			'bookedTillTime': -1
		}
	]

	testCars4 = [
		{
			'id': 1,
			'x': 10,
			'y': 10,
			'booked': True,
			'bookedTillTime': 100
		},
		{
			'id': 2,
			'x': -60,
			'y': -60,
			'booked': False,
			'bookedTillTime': -1
		},
		{
			'id': 3,
			'x': 30,
			'y': -10,
			'booked': False,
			'bookedTillTime': -1
		}
	]

	testCars5 = [
		{
			'id': 1,
			'x': 10,
			'y': 10,
			'booked': True,
			'bookedTillTime': 100
		},
		{
			'id': 2,
			'x': -60,
			'y': -60,
			'booked': True,
			'bookedTillTime': 100
		},
		{
			'id': 3,
			'x': 30,
			'y': -10,
			'booked': True,
			'bookedTillTime': 100
		}
	]
	return testCars1,testCars2, testCars3, testCars4,testCars5

"""
A car can be in quadrant 
		(+ve)
		  |
	A	  |     B
------- (0,0) -------	(+ve)
	C	  |     D
		  |
"""
def prepPointsForTesting():

	testSourceA = [ 
		{
			'x': -10,
			'y': 10,
		},
		{
			'x': -50,
			'y': 40
		}
	]
	testSourceB = [ 
		{
			'x': 10,
			'y': 10,
		},
		{
			'x': 50,
			'y': 40
		}
	]
	testSourceC = [ 
		{
			'x': -10,
			'y': -10,
		},
		{
			'x': -60,
			'y': -60
		}
	]
	testSourceD = [ 
		{
			'x': 30,
			'y': -10,
		},
		{
			'x': 20,
			'y': -20
		}
	]

	return testSourceA,testSourceB,testSourceC,testSourceD



def test_time_travel():
	#setup points for testing
	testSourceA,testSourceB,testSourceC,testSourceD = prepPointsForTesting()

	#From A0 to B1
	assert timeTakenFromAtoB(testSourceA[0],testSourceB[1]) == 90
	#From D0 to A1
	assert timeTakenFromAtoB(testSourceD[0],testSourceA[1]) == 130
	#From A0 to C1
	assert timeTakenFromAtoB(testSourceA[0],testSourceC[1]) == 120
	#From C1 to B0
	assert timeTakenFromAtoB(testSourceC[1],testSourceB[0]) == 140
	#From D0 to C0
	assert timeTakenFromAtoB(testSourceD[0],testSourceC[0]) == 40
	#From B1 to D0
	assert timeTakenFromAtoB(testSourceB[1],testSourceD[0]) == 70


def test_find_a_suitable_car():
	testCars1,testCars2, testCars3, testCars4,testCars5 = prepCars()
	testSourceA,testSourceB,testSourceC,testSourceD = prepPointsForTesting()

	# if 2 cars are on the same location the smallest id car should be picked
	assert findASuitableCar(testSourceA[0],testCars1) == (1020,1)
	#test if the car is picked assuming cars and customer are in different quadrants
	assert findASuitableCar(testSourceA[1],testCars2) == (90,1)
	#test if the nearest car is picked followed by id of the car
	assert findASuitableCar(testSourceA[1],testCars3) == (90,3)
	#car 1 that is the nearest has been booked
	assert findASuitableCar(testSourceA[1],testCars4) == (110,2)
	# all the cars have been booked
	assert findASuitableCar(testSourceA[1],testCars5) == (-1,-1)

if __name__ == '__main__':
	app.run(debug=True)
