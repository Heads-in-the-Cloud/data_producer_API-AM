import requests
from Producers import UsersProducer, FlightsProducer, BookingsProducer

# globals
uri_list = {'users': "https://localhost:8443",
            'flights': "http://localhost:8081",
            'bookings': "http://localhost:8082"}

user_insert_size = 1000
flight_insert_size = 1000
booking_insert_size = 1000

HEADER_STRING = "Authorization"
admin = {'username': 'admin',
         'password': 'pass'}


if __name__ == '__main__':
    # get jwt token for admin login
    jwt = requests.post(uri_list['users'] + "/login", json=admin, verify=False).headers[HEADER_STRING][7:]
    token = {'Authorization': 'Bearer {}'.format(jwt)}

    # run producer
    UsersProducer.run(uri_list, token, user_insert_size)
    FlightsProducer.run(uri_list, token, flight_insert_size)
    BookingsProducer.run(uri_list, token, booking_insert_size)
