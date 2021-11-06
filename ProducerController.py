import requests
import urllib3
import os
from Producers import UsersProducer, FlightsProducer, BookingsProducer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#########################
# Environment Variables #
#########################

uri_list = {'users': os.environ['uri_users'],
            'flights': os.environ['uri_flights'],
            'bookings': os.environ['uri_bookings']}

sizes = [int(os.environ['size_users']),
         int(os.environ['size_users']),
         int(os.environ['size_users'])]

HEADER_STRING = os.environ['jwt_header']

debug = bool(os.environ['debug'])


######################
# Producer Functions #
######################

def users_producer(uri, jwt_token, size):
    UsersProducer.run(uri, jwt_token, size, debug)


def flights_producer(uri, jwt_token, size):
    FlightsProducer.run(uri, jwt_token, size, debug)


def bookings_producer(uri, jwt_token, size):
    BookingsProducer.run(uri, jwt_token, size, debug)


options_list = "\nAvailable Data Producers:\n" \
               "  1: Users Producer\n" \
               "  2: Flights Producer\n" \
               "  3: Bookings Producer\n" \
               "  4: Exit\n"
options = {1: users_producer,
           2: flights_producer,
           3: bookings_producer}

##############
# ## MAIN ## #
##############

if __name__ == '__main__':

    ##############
    # Login Loop #
    ##############

    print("ADMIN LOGIN")
    while True:
        username = input("Username:\n - ")
        password = input("Password:\n - ")
        admin = {'username': username,
                 'password': password}

        #################
        # Get JWT Token #
        #################

        print("Fetching JWT Token...")
        token = None

        try:
            jwt = requests.post(uri_list['users'] + "/login", json=admin, verify=False).headers[HEADER_STRING][7:]
            token = {'Authorization': 'Bearer {}'.format(jwt)}
        except requests.ConnectionError:
            # catch failed to connect
            print("Unable to connect to the server. Confirm that the Authentication server is running.")
            exit(1)
        except KeyError:
            # catch invalid login
            print("Incorrect login. Please try again.")
            continue
        else:
            # success
            print("JWT Token received.")
            break

    ###################
    # Production Loop #
    ###################

    print(options_list)
    while True:

        ###################
        # Select Producer #
        ###################

        # guarantee selection is an integer
        select = None
        try:
            select = int(input("Please select which producer to run.\n - "))
        except ValueError:
            print("Please enter an Integer value.\n")
            continue

        #################
        # Run Producers #
        #################

        # check exit code
        if select == 4:
            print("Exiting...")
            exit(0)

        # guarantee selection is within range
        if select not in options.keys():
            print("Option " + str(select) + " is not a valid option. Please enter a valid option.")
            continue
        options[select](uri_list, token, sizes[select])

        # re-print options for new loop
        print(options_list)
