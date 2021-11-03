import requests
from faker import Faker


def run(uri, token, size):
    # faker
    fake = Faker('en_US')

    # users
    users = []
    for i in range(round(size * .75)):
        firstname = fake.first_name_nonbinary()
        user = {'roleId': 1,
                'givenName': firstname,
                'familyName': fake.last_name(),
                'username': firstname + "_" + fake.pystr(3, 3),
                'password': fake.pystr(8, 12),
                'email': fake.ascii_free_email(),
                'phone': fake.phone_number()}
        users.append(user)

    # agents
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
    response = requests.post(uri['users'] + '/api/v1/users/post', json=users, verify=False, headers=token)
    print(response.text)
