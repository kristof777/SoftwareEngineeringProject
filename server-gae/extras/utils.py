import sys
sys.path.append("../")
import random
import string
import webapp2
import json
import Main
from validate_email import validate_email


def get_random_string(n=random.randint(10,20), lower_case=0, upper_case=0,
                      numbers=0):
    """
    Function takes the integer, and return a random string of that length, which
    contains n characters, with lower_case lower case characters, upper_case
    upper case characters and numbers numbers.
    :param n: representing the lenth of desired random string:
    :param lower_case: number of desired lower case letters in random string
    :param upper_case: number of desired upper case letters in random string
    :param numbers: number of desired numbers in random string
    :return: a random string
    """
    s = ""
    if lower_case == upper_case == numbers == 0:
        s = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase) for _
                in range(n))
    else:
        new_n = n - lower_case - upper_case - numbers
        if new_n > 0:
            s = ''.join(random.SystemRandom().choice(
                string.ascii_uppercase + string.digits + string.ascii_lowercase)
                        for _
                        in range(new_n))
        s += ''.join(random.SystemRandom().choice(string.ascii_lowercase)
                        for _
                        in range(lower_case))
        s += ''.join(random.SystemRandom().choice(string.ascii_uppercase)
                     for _
                     in range(upper_case))
        s += ''.join(random.SystemRandom().choice(string.digits)
                     for _
                     in range(numbers))

    return s


def get_random_email():
    """
    Return the random valid email, in format <a>@<b>.ca
     where <a> is of length in between 6 and 12
           <b> is of length in between 4 and 12
    :return: a string representing email
    """

    return get_random_string(random.randint(6, 12)) + "@" \
        + get_random_string(random.randint(4, 12)) + ".ca"


def get_random_password():
    """
    a random password
    :return: a string containing a random password
    """

    return get_random_string(random.randint(8, 16), 1, 1, 1)


def test_random_email():
    """
    #TODO
    :return:
    """
    for i in range(0, 10):
        email = get_random_email()
        testing_email = email.split("@")
        assert len(testing_email) == 2
        assert testing_email[1][-3:] == ".ca"
        email = testing_email[0] + testing_email[1][:-3]
        assert email.isalnum()


def test_random_password():
    """
    #TODO
    :return:
    """
    for i in range(0, 10):
        password = get_random_password()
        assert len(password) >= 8
        assert password.isalnum()
        assert any(s.islower() for s in password)
        assert any(s.isupper() for s in password)
        assert any(s.isdigit() for s in password)


def create_dummy_users_for_testing(n):
    """
    Crates n Dummy Users with random valid password, email, first name,
     last name, city, postalCode, phone number1, phone number2 (optionally)
     "SK" as a province, userId, and a token

    :param n: number of dummy users required.
    :return: a dictionary of user with email, first name,
     last name, city, postalCode, phone number1, phone number2 (optionally)
     "SK" as a province, userId, and a token as keys.
    """
    users = []
    while n > 0:
        password = get_random_password()
        new_user = {"email": get_random_email(),
                  "password": password ,
                  "firstName": get_random_string(),
                  "lastName": get_random_string(),
                  "city": get_random_string(),
                  "postalCode": get_random_string(3)+" "+get_random_string(3),
                  "province": "SK",
                  "phone1": get_random_string(10, numbers=10),
                   "phone2": get_random_string(10, numbers=10)
                   if random.randint(0,1) else "",
                  "confirmedPassword": password
                  }

        request = webapp2.Request.blank('/createuser', POST=new_user)  # api you need to test
        response = request.get_response(Main.app)
        output = json.loads(response.body)
        del new_user["confirmedPassword"]
        del new_user["password"]
        new_user["token"] = str(output["token"])
        new_user["userId"] = str(output["userId"])
        users.append(new_user)
        n -= 1
    return users


def create_dummy_listings_for_testing(num_listings, num_users=1):
    """
    Crates n Dummy Users and listings, where all data in listings is random but
    province which is saskatchewan.

    :param num_listings: number of dummy listing required.
    :param num_users: number of users, in which listing needs to be distributed
    :return: a dictionary of listing with all listing data as keys and listingID
     """
    listings = []
    assert num_listings > num_users
    assert num_users != 0

    users = create_dummy_users_for_testing(num_users)
    assert len(users) == num_users
    for i in range(0, num_users):
        if i == num_users - 1 and num_listings % num_users != 0:
            distribution = num_listings // num_users + 1
        else:
            distribution = num_listings // num_users
        user = users[i]
        for j in range(0, distribution):
            random_listing_info = { "userId": user["userId"],
                      "bedrooms": str(random.randint(1,10)),
                      "sqft": str(random.randint(200,2000)),
                      "bathrooms": str(random.randint(1,10)),
                      "price": str(random.randint(20000,20000000)),
                      "description": " ".join(
                          [get_random_string() for _ in
                           range(random.randint(15, 45))]) + ".",
                      "isPublished": str(bool(random.randint(0, 1))),
                      "province": "SK",
                      "city": get_random_string(),
                      "address": get_random_string(),
                      "thumbnailImageIndex": 0,
                      "images": 'some images'
                      }
            request = webapp2.Request.blank('/createlisting',
                                        POST=random_listing_info)
            response = request.get_response(Main.app)
            output = json.loads(response.body)
            random_listing_info["listingId"] = output["listingId"]
            listings.append(random_listing_info)

    return listings, users


def create_random_user():
    """
    :return: a random user with random field populated
    """

    password = get_random_password()
    user = {"email": get_random_email(),
            "password": password,
            "firstName": get_random_string(),
            "lastName": get_random_string(),
            "city": get_random_string(),
            "province": "SK",
            "phone1": get_random_string(10, numbers=10),
            "phone2": get_random_string(10, numbers=10)
            if random.randint(0, 1) else "", "confirmedPassword": password}
    return user


def create_random_listing(user_id):
    """
    :param user_id: User Id where listing belongs
    :return: a random listing with random field populated
    """
    random_listing = { "userId": user_id,
                      "bedrooms": str(random.randint(1,10)),
                      "sqft": str(random.randint(200,2000)),
                      "bathrooms": str(random.randint(1,10)),
                      "price": str(random.randint(20000,20000000)),
                      "description": " ".join(
                          [get_random_string() for _ in
                           range(random.randint(15, 45))]) + ".",
                      "isPublished": str(bool(random.randint(0, 1))),
                      "province": "SK",
                      "city": get_random_string(),
                      "address": get_random_string(),
                      "thumbnailImageIndex": 0,
                      "images": 'some images'
                      }
    return random_listing


def keys_validation(key_error_dict, post):
    """
    Example :
    key_error_dict = {"password": "missingPassword",
    "confirmedPassword": "missingConfirmedPassword"}
    post = {}
    then
    error will be {"missingPassword": "Password is missing",
    "missingConfirmedPassword": "confirmedPassowrd is missing"}
    values = {}
    :param key_error_dict: Takes a key error dictionary
    :param post: Post request
    :return: errors and post values converted to string
    """
    errors = {}
    values = {}
    empty = [u'', '', ""]
    for key in key_error_dict:
        error = key_error_dict[key]["error"]
        value_in_response = post.get(key)
        if value_in_response is None or str(value_in_response).isspace()\
                or str(value_in_response) in empty:
            errors[error] = str(key) + " is Missing"
        else:
            values[key] = str(value_in_response)
    return errors, values


def is_valid_phone(phone):
    """

    :param phone:
    :return: true if phone number is Valid
    """
    assert phone != None
    return len(phone) == 10 and unicode(phone,'utf-8').isnumeric()


def is_invalid_password(password):
    """

    :param password:
    :return: true if password is valid
    """
    return len(password) < 8 or not any(s.islower() for s in password) or \
           not any(s.isupper() for s in password) or \
           not any(s.isdigit() for s in password)


def is_valid_email(email):
    """
    :param email:
    :return: True is email is valid
    """
    return validate_email(email)


def test_keys_validation():
    keys = ["key1", "key2", "key3"]
    errors = ["error1", "error2", "error3"]
    key_error_dict = dict(zip(keys,errors))
    response = {"key1": "a", "key2": "b", "key3": u'    '}
    print(keys_validation(key_error_dict, response))
    response = {"key1": "a", "key2": "b", "key3": u''}
    print(keys_validation(key_error_dict, response))
    response = {"key1": "a", "key2": "", "key3": u''}
    print(keys_validation(key_error_dict, response))
    response = {"key1": "a", "key2": "", "key3": u'    '}
    print(keys_validation(key_error_dict, response))


if __name__ == "__main__":
    test_random_email()
    test_random_password()
    test_keys_validation()

