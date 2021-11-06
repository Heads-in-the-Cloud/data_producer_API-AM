import requests
import json
import time
from faker import Faker
from random import randint, seed


def run(uri, token, size, debug):

    # faker
    fake = Faker('en_US')
    seed(time.process_time())

    ################
    # COLLECT DATA #
    ################

    # users
    users_list = json.loads(requests.get(uri['users'] + '/api/v1/users/role/1', verify=False, headers=token).text)
    users = []
    for user in users_list:
        users.append(user['id'])
    if debug:
        print('user IDs:', users)

    # flights
    flights_list = json.loads(requests.get(uri['flights'] + '/api/v1/flights', verify=False, headers=token).text)
    flights = []
    for flight in flights_list:
        flights.append(flight['id'])
    if debug:
        print('flight IDs:', flights)

    # agents
    agents_list = json.loads(requests.get(uri['users'] + '/api/v1/users/role/2', verify=False, headers=token).text)
    agents = []
    for agent in agents_list:
        agents.append(agent['id'])
    if debug:
        print('agent IDs:', agents)

    #################
    # GENERATE DATA #
    #################

    # bookings for users
    for i in range(round(size * .66)):
        booking = {'isActive': 1,
                   'confirmationCode': fake.pystr(10, 10),
                   'flightId': flights[randint(0, len(flights) - 1)],
                   'agentId': agents[randint(0, len(agents) - 1)],
                   'userId': users[randint(0, len(users) - 1)]}
        requests.post(uri['bookings'] + '/api/v1/bookings', json=booking, verify=False, headers=token)

    # bookings for guests
    for i in range(round(size * .33)):
        booking = {'isActive': 1,
                   'confirmationCode': fake.pystr(10, 10),
                   'flightId': flights[randint(0, len(flights) - 1)],
                   'agentId': agents[randint(0, len(agents) - 1)],
                   'guestEmail': fake.ascii_free_email(),
                   'guestPhone': fake.phone_number()}
        requests.post(uri['bookings'] + '/api/v1/bookings', json=booking, verify=False, headers=token)

    ###############
    # RESULT DATA #
    ###############

    # result bookings
    bookings_list = json.loads(requests.get(uri['bookings'] + '/api/v1/bookings', verify=False, headers=token).text)
    bookings = []
    for booking in bookings_list:
        if not booking['passengers']:
            bookings.append(booking['id'])
    if debug:
        print('booking IDs:', bookings)

    ###################
    # CONTINGENT DATA #
    ###################

    for booking in bookings:
        # passengers
        genders = ['Male', 'Female', 'Other', 'Not Specified']
        for i in range(randint(1, 4)):
            # create passenger
            lastname = fake.last_name()
            passenger = {'bookingId': booking,
                         'givenName': fake.first_name_nonbinary(),
                         'familyName': lastname,
                         'dob': fake.date(),
                         'gender': genders[randint(0, 3)],
                         'address': fake.address()[0:44]}
            requests.post(uri['bookings'] + '/api/v1/passengers', json=passenger, verify=False, headers=token)

        # payment
        payment = {'bookingId': booking,
                   'stripeId': fake.pystr(10, 10),
                   'refunded': 0}
        response = requests.post(uri['bookings'] + '/api/v1/payments', json=payment, verify=False, headers=token)
        if debug:
            print(response.text)
