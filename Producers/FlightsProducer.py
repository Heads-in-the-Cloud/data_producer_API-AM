import requests
from faker import Faker
import json
from random import randint, uniform


def run(uri, token, size, debug):
    # faker
    fake = Faker('en_US')

    # airports
    for i in range(20):
        airport = {'city': fake.city(),
                   'iataId': fake.pystr(3, 3).upper()}
        requests.post(uri['flights'] + '/api/v1/airports', json=airport, verify=False, headers=token)

    # routes (uses airports)
    airports_info = json.loads(requests.get(uri['flights'] + '/api/v1/airports', verify=False, headers=token).text)
    airports = []
    for airport in airports_info:
        airports.append(airport['id'])
    for i in range(50):
        origin = airports[randint(0, len(airports) - 1)]
        destination = airports[randint(0, len(airports) - 1)]
        if origin != destination:
            route = {'origin': origin,
                     'destination': destination}
            requests.post(uri['flights'] + '/api/v1/routes', json=route, verify=False, headers=token)

    # airplane types
    for i in range(10):
        airplane_type = {'maxCapacity': (i * 20) + 100}
        requests.post(uri['flights'] + '/api/v1/airplaneTypes', json=airplane_type, verify=False, headers=token)

    # airplanes (uses airplane types)
    types_info = json.loads(requests.get(uri['flights'] + '/api/v1/airplaneTypes', verify=False, headers=token).text)
    types = []
    for type_num in types_info:
        types.append(type_num['id'])
    for i in range(20):
        airplane = {'airplaneType': types[randint(0, len(types) - 1)]}
        requests.post(uri['flights'] + '/api/v1/airplanes', json=airplane, verify=False, headers=token)

    # flights (uses routes and airplanes)
    routes_info = json.loads(requests.get(uri['flights'] + '/api/v1/routes', verify=False, headers=token).text)
    airplanes_info = json.loads(requests.get(uri['flights'] + '/api/v1/airplanes', verify=False, headers=token).text)
    routes = []
    airplanes = []
    for route in routes_info:
        routes.append(route['id'])
    for airplane in airplanes_info:
        airplanes.append(airplane['id'])
    for i in range(size):
        flight = {'route': routes[randint(0, len(routes) - 1)],
                  'airplane': airplanes[randint(0, len(airplanes) - 1)],
                  'dateTime': fake.date() + 'T' + fake.time('%H:%M'),
                  'reservedSeats': 0,
                  'seatPrice': round(uniform(100.0, 300.0), 2)}
        requests.post(uri['flights'] + '/api/v1/flights', json=flight, verify=False, headers=token)
