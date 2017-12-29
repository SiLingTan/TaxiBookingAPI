
"""
Name: Tan Si Ling
Date Implemented : 28th December 2017

Program: Taxi Booking System

"""

#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_httpauth import HTTPBasicAuth


""" ********** Basic API Authorisation Handler ********** """
#This is for the booking of a taxi, to extend to other APIs in future

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
	if username == 'TaxiCustomerA':
		return 'CustA123'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access. Please try again.'}), 401)



""" ********** Main program ********** """

app = Flask(__name__)
systemTime = 0;

cars = [
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
		'booked': False,
		'bookedTillTime': -1
	},
	{
		'id': 3,
		'x': 1000,
		'y': 0,
		'booked': False,
		'bookedTillTime': -1
	}
]

@app.route('/api/tick', methods=['POST'])
def incrementSystemTime():
	global systemTime
	systemTime += 1

	#if the car has reached its destination, set it to be available
	#At the next unit time, do we free up this car
	for car in cars:
		if(car['bookedTillTime'] + 1 == systemTime):
			car['booked'] = False

	#For unit test
	#return systemTime
	return jsonify({'tick': systemTime})


@app.route('/api/reset', methods=['POST'])
def resetTaxiSystem():
	global systemTime
	systemTime = 0

	for car in cars:
		car['x'] = 0
		car['y'] = 0
		car['booked'] = False
		car['bookedTillTime'] = -1

	#For unit test
	#return systemTime
	return jsonify({'tick': systemTime})

# Calculates time taken to travel from source A (x1, y1) to destination (x2,y2)
# where source (x1, y1) is represeneted as source['x'] and source['y'] respectively
def timeTakenFromAtoB(source, dest):
	return abs(dest['x'] - source['x']) + abs(dest['y'] - source['y'])


# Given the customer's current position and the position of all taxi cars that are currently available, 
# return the nearest taxi car with the smallest id
def findASuitableCar(custSourcePosition, taxiCars):
	
	timeForCarsToSouce = []

	for car in taxiCars:
		if(car['booked'] == False):
			timeToTravelToCustomer = timeTakenFromAtoB(car, custSourcePosition) 
			timeForCarsToSouce.append({timeToTravelToCustomer:car['id']})


	if(len(timeForCarsToSouce) != 0):
		# select the nearest car to the customer and remove the {} brackets
		selectedCar = str(sorted(timeForCarsToSouce)[0])[1:-1]
		#time for car to travel to customer's source
		timeCarToCustSource = int(selectedCar.split(":")[0])
		carID = int(selectedCar.split(":")[1])

		return timeCarToCustSource,carID

	return -1,-1



@app.route('/api/book', methods=['POST'])
@auth.login_required
def bookATaxi():
	if not request.json or not 'source' in request.json or not 'destination' in request.json:
		abort(400)
	if 'source' in request.json and ((type(request.json['source']['x']) is not int) or (type(request.json['source']['y']) is not int)):
		abort(400)
	if 'destination' in request.json and ((type(request.json['destination']['x']) is not int) or (type(request.json['destination']['y']) is not int)):
		abort(400)

	source = request.json['source']
	dest = request.json['destination']

	#time need to take customer from source to destination
	timeCustSourceToDest = timeTakenFromAtoB(source, dest) 

	#time needed for the nearest car to reach customer's source
	timeCarToCustSource,carID = findASuitableCar(source,cars)

	for car in cars:
		#Check if the car is booked
		if(car['id'] == carID):	
			car['booked'] = True
			#place the car at dest coordinates since it is booked anyway
			car['x'] = dest['x']
			car['y'] = dest['y']
			car['bookedTillTime'] = timeCarToCustSource + timeCustSourceToDest + systemTime 
			return jsonify({'car_id': carID, 'total_time': timeCarToCustSource + timeCustSourceToDest}), 201	

	return jsonify({})


# modify error handler for 404 to return json instead of html
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=False)
