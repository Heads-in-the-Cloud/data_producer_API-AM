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
         int(os.environ['size_flights']),
         int(os.environ['size_bookings'])]

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


def all_producers(uri, jwt_token, prod_sizes):
    UsersProducer.run(uri, jwt_token, prod_sizes[0], debug)
    FlightsProducer.run(uri, jwt_token, prod_sizes[1], debug)
    BookingsProducer.run(uri, jwt_token, prod_sizes[2], debug)


options_list = "\nAvailable Options:\n" \
               "  1: Run Users Producer\n" \
               "  2: Run Flights Producer\n" \
               "  3: Run Bookings Producer\n" \
               "  4: Run All Producers\n" \
               "  5: Exit\n"
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
            print("Unable to connect to Authentication servers. Please confirm "
                  "that the Authentication server is running.")
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

        # exit code option
        if select == 5:
            print("Exiting...")
            exit(0)

        # all data producers option
        if select == 4:
            all_producers(uri_list, token, sizes)
            print(options_list)
            continue

        # guarantee selection is otherwise within range and run
        if select not in options.keys():
            print(f"Option '{select}' is not a valid option. Please enter a valid option.")
            continue
        options[select](uri_list, token, sizes[select - 1])

        # re-print options for new loop
        print(options_list)
