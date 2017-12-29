Taxi Booking System
==============
Provides Taxi Booking APIs in a 2D Grid World.


Pre-requisities 
---------------
1. Download [Postman](https://www.getpostman.com/postman)
2. Unzip the source code (TaxiServiceApi.zip) and place it into your local path directory.
3. Install Python (my version 2.7.5)
4. Install [virtualenv](https://pypi.python.org/pypi/virtualenv) 

```cmd
$ cd TaxiServiceApi
$ virtualenv flask
$ pip install flask
```

Run the Program
---------------
1. Navigate into your TaxiServiceApi folder and run app.py.

```cmd
$ python app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

2. Launch your postman and type http://TaxiCustomerA:CustA123@localhost:5000/api/book to fire a request.

```
Note: For authorization of “Book a Taxi” API, please use the following credentials.
Client ID: TaxiCustomerA
Client Secret: CustA123
```

More Information
-------------------
- [API Interface Documentation](https://github.com/SiLingTan/TaxiBookingAPI/blob/master/Taxi%20Booking%20System%20API%20Document_v0.1.pdf)
- [API Design Documentation](https://github.com/SiLingTan/TaxiBookingAPI/blob/master/Taxi%20Booking%20System%20Design%20Document_v0.1.pdf)
