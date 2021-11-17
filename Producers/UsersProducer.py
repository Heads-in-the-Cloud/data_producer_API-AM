import requests
from faker import Faker


def run(uri, token, size, debug):

    ###########
    # Startup #
    ###########

    fake = Faker('en_US')
    print("Starting Users Data Producer.")
    users_size = round(size * .75)
    agents_size = size - users_size

    ################
    # Confirmation #
    ################

    try:
        requests.get(uri['users'], verify=False, headers=token)
    except requests.ConnectionError:
        print("Error connecting to Users service! Is the service running?")
        exit(1)
    else:
        if debug:
            print("Successfully connected to Users service.")

    #########################
    # Generate Normal Users #
    #########################

    if debug:
        print("Generating " + str(users_size) + " Users...")
    users = []
    for i in range(users_size):
        firstname = fake.first_name_nonbinary()
        user = {'roleId': 1,
                'givenName': firstname,
                'familyName': fake.last_name(),
                'username': firstname + "_" + fake.pystr(3, 3),
                'password': fake.pystr(8, 12),
                'email': fake.ascii_free_email(),
                'phone': fake.phone_number()}
        users.append(user)
    if debug:
        print("Users Generated.")

    #####################
    # Generate Agents #
    #####################

    if debug:
        print("Generating " + str(agents_size) + " Agents...")
    for i in range(round(size * .25)):
        firstname = fake.first_name_nonbinary()
        user = {'roleId': 2,
                'givenName': firstname,
                'familyName': fake.last_name(),
                'username': firstname + "_" + fake.pystr(3, 3) + "_agent",
                'password': fake.pystr(8, 12),
                'email': fake.ascii_free_email(),
                'phone': fake.phone_number()}
        users.append(user)
    if debug:
        print("Agents Generated.")

    #############
    # Send Data #
    #############

    response = requests.post(uri['users'] + '/api/v1/users/post', json=users, verify=False, headers=token)
    if debug:
        print(response.text)
    if response.status_code != 204:
        print("There was an error inserting into the Users database. Exiting...")
        exit(1)
    print("Users successfully added.")
