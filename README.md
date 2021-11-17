# Data Producers Repository

This repository contains the scripts for each of the Data Producers, along with a producer controller to call them. 

When running the producer, several environment variables must be specified:
* uri_users (users API endpoint: i.e., http://localhost:8080)
* uri_flights (flights API endpoint)
* uri_bookings (bookings API endpoint)
* size_users (number of users to insert)
* size_flights (number of flights to insert)
* size_bookings (number of bookings to insert)
* jwt_header (identifier for JWT headers, such as 'Authorization')
* debug (True or False, enables verbose output)
* PYTHONUNBUFFERED (optional, performance increase)
