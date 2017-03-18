import random
import string
import webapp2
import json
from Error_Code import *
from models.User import *
from validate_email import validate_email
from google.appengine.ext import testbed
import re


"""
province_abbr and province_complete are all the provinces of canada,
province_abbr have abbreviations of provinces, where as province_complete has
complete names of the provinces. Province at index i represents the same
province.
"""
province_abbr = ["AB", "BC", "MB", "NB", "NL", "NS", "NU", "NW", "ON", "PE",
                 "QC", "SK", "YT"]

province_complete = ["alberta", "british columbia", "manitoba", "new brunswick",
                     "newfoundland and labrador", "nova scotia", "nunavut",
                     "north west territories", "ontario",
                     "prince edward island", "quebec", "saskatchewan", "yukon"]


"""
listing_keys contains all the valid keys for a listing
"""
listing_keys = ["userId", "squarefeet", "bedrooms", "bathrooms", "price", "city", "province",
                "address", "description", "isPublished", "images",
                "thumbnailImageIndex", "latitude", "longitude", "postalCode", "authToken"]


def get_random_string(n=random.randint(10, 20), lower_case=0, upper_case=0,
                      numbers=0):
    """
    Creates a random string with the given properties
    :param n: lenth
    :param lower_case: number of lower case characters
    :param upper_case: number of upper case characters
    :param numbers: number of numeric characters
    :return: a random string
    """
    s = ""
    if lower_case == upper_case == numbers == 0:
        s = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits + string.ascii_lowercase) for
                    _
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

    return get_random_string(random.randint(6, 12)) + "@" + \
        get_random_string(random.randint(4, 6)) + ".ca"


def get_random_password():
    """
    a random password
    :return: a string containing a random password
    """

    return get_random_string(random.randint(8, 16), 1, 1, 1)

def get_random_postal_code():
    """
    a random postalCode
    :return: a string containing a random password
    """
    postalCode = ''
    for i in range(0,3):
        postalCode += (get_random_string(1, 0, 1, 0) + str(random.randint(0,9)))
    return postalCode


def create_dummy_users_for_testing(main, n):
    """
     Creates n dummy users with random values.
    :param main: Main handler, to make an api call.
    :param n: number of dummy users required.
    :return: a dictionary containing: email, first name,
     last name, city, postalCode, phone number1, phone number2 (optionally)
     "SK" as a province, userId, and a token as keys.
    """
    users = []
    while n > 0:
        password = get_random_password()
        new_user = {"email": get_random_email(),
                    "password": password,
                    "firstName": get_random_string(),
                    "lastName": get_random_string(),
                    "city": get_random_string(),
                    "province": "SK",
                    "phone1": get_random_string(10, numbers=10),
                    "phone2": get_random_string(10, numbers=10)
                    if random.randint(0, 1) else "",
                    "confirmedPassword": password
                    }
        request = webapp2.Request.blank('/createUser', POST=new_user)
        response = request.get_response(main.app)
        output = json.loads(response.body)
        del new_user["confirmedPassword"]
        del new_user["password"]
        new_user["authToken"] = str(output["authToken"])
        new_user["userId"] = str(output["userId"])
        users.append(new_user)
        n -= 1
    return users


def create_dummy_listings_for_testing(main, num_listings, num_users=1):
    """
    Creates n dummy users and listings. All of the fields will be randomized,
    with the exception of Province, which will be Saskatchewan

    :param main: Main handler
    :param num_listings: number of dummy listing to create
    :param num_users: number of users to assign listings to
    :return: a dictionary of listing with all listing data as keys and listingID
     """
    listings = []
    assert num_listings >= num_users
    assert num_users != 0

    users = create_dummy_users_for_testing(main, num_users)
    assert len(users) == num_users
    for i in range(0, num_users):
        if i == num_users - 1 and num_listings % num_users != 0:
            distribution = num_listings // num_users + 1
        else:
            distribution = num_listings // num_users
        user = users[i]
        for j in range(0, distribution):
            random_listing_info = {"userId": user["userId"],
                                   "authToken": user["authToken"],
                                   "bedrooms": str(random.randint(1, 10)),
                                   "longitude": str(random.randint(-180, 180)),
                                   "latitude": str(random.randint(-90, 90)),
                                   "postalCode": get_random_postal_code(),
                                   "squarefeet": str(random.randint(200, 2000)),
                                   "bathrooms": str(random.randint(1, 10)),
                                   "price": str(
                                       random.randint(20000, 20000000)),
                                   "description": " ".join(
                                       [get_random_string() for _ in
                                        range(random.randint(15, 45))]) + ".",
                                   "isPublished": str(
                                       bool(random.randint(0, 1))),
                                   "province": "SK",
                                   "city": get_random_string(),
                                   "address": get_random_string(),
                                   "thumbnailImageIndex": 0,
                                   "images": json.dumps(['some images',
                                                         'some images 2'])
                                   }

            request = webapp2.Request.blank('/createListing',
                                            POST=random_listing_info)
            response = request.get_response(main.app)
            output = json.loads(response.body)
            random_listing_info["listingId"] = output["listingId"]
            listings.append(random_listing_info)

    return listings, users

def create_random_user():
    """
    :return: a randomly generated user profile
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

def create_random_listing(user_id, token):
    """
    :param user_id: User Id where listing belongs
    :return: a listing with randomly generated fields
    """
    random_listing = {"userId": user_id,
                      "authToken": token,
                      "bedrooms": str(random.randint(1, 10)),
                      "longitude": str(random.randint(-180, 180)),
                      "latitude": str(random.randint(-90, 90)),
                      "postalCode": get_random_postal_code(),
                      "squarefeet": str(random.randint(50, 12000)),
                      "bathrooms": str(random.randint(1, 10)),
                      "price": str(random.randint(100000, 2000000)),
                      "description": " ".join(
                          [get_random_string() for _ in
                           range(random.randint(15, 45))]) + ".",
                      "isPublished": str(bool(random.randint(0, 1))),
                      "province": "SK",
                      "city": get_random_string(),
                      "address": get_random_string(),
                      "thumbnailImageIndex": 0,
                      "images": json.dumps(['some images', 'some images 2'])
                      }
    return random_listing


def keys_missing(required_keys, post):
    """
    Example :
    required_keys = [ "missingPassword", "confirmedPassword" ]
    post = {}

    errors will be {"missingPassword": "Password is missing",
    "missingConfirmedPassword": "confirmedPassowrd is missing"}
    values = {}

    :param required_keys: List of keys
    :param post: Post request
    :return: errors and post values converted to string
    """
    errors = {}
    values = {}

    #  find if anything is missing for not
    for key in required_keys:
        error = missing[key]['error']
        value_in_response = post.get(key)
        if is_empty(value_in_response):
            errors[error] = str(key) + " is Missing"
        else:
            values[key] = str(value_in_response)

    # If any key present in post, which is not required, converted to values.
    for key in post:
        if key not in errors and key not in values:
            values[key] = post.get(key)

    return errors, values


def key_validation(dictionary):
    """
    Checks the validity a dictionary of keys.
    :param dictionary: Dictionary containing:  phone1, phone2, email,
    password, province, userId, listingId, price, bathrooms, bedrooms, sqft,
    isPublished, thumbnailImageIndex, liked, valuesRequired, maxLimit,
    listingIdList, lower, upper

    Everything not in the list is considered as valid
    :return: a dictionary containing all invalid keys.
    """
    invalid = {}
    for key in dictionary:
        value = dictionary[key]
        if is_empty(value):
            continue
        if key in valid_check:
            if not valid_check[key](value):
                invalid[invalids[key]["error"]] = key + " is invalid"
    return invalid


def is_valid_integer(input_string):
    """
    Checks if input_string is an integer
    :param input_string: A number or a string.
    :return: True if integer, otherwise false
    """

    assert input_string is not None
    try:
        int(input_string)
        return True
    except ValueError:
        return False


def is_valid_float(input_string):
    """
    :param input_string: A floating number
    :return: True if float, otherwise false
    """
    assert input_string is not None
    try:
        value = float(input_string)
        return True
    except ValueError:
        return False


def is_valid_bathroom(input_string):
    """

    Checks if input_string is float or not
    :param input_string: A number or a string.
    :return: True if float, otherwise false
    """
    assert input_string is not None
    try:
        br = float(input_string)
        if round(br) - br == 0 or round(br) - br == 0.5:
            return True
        else:
            return False
    except ValueError:
        return False


def is_valid_bool(input_string):
    """
    Checks if input_string is boolean or not
    :param input_string: A number or a string.
    :return: True if boolean, otherwise false
    """
    assert input_string is not None
    if input_string in ['true', "True", "TRUE", '1', "t", "y", "yes", "false", "False", "FALSE", "0", "n", "no", "N"]:
        return True
    else:
        return False


def is_valid_phone(phone):
    """
    Checks if phone is valid phone or not. Valid here means, if it is of 10
    digits or not.
    :param phone: A number or a string.
    :return: True if a valid phone number, otherwise false
    """
    assert phone is not None
    phone = str(phone)
    return len(phone) == 10 and is_valid_integer(phone)


def is_valid_password(password):
    """
    Checks if password is a valid password or not. Valid passwords are >=8,
    and have at least one lower-case, upper-case, and numeric character.
    :param password: String to be checked
    :return: true if password is valid, otherwise false
    """
    return len(password) >= 8 and any(s.islower() for s in password) \
           and any(s.isupper() for s in password) \
           and any(s.isdigit() for s in password)


def is_valid_string_listing(listing):
    """
    Checks if all the key is listing dictionary are contained in listing_keys
    :param listing: a listing dictionary
    :return: true if listing dictionary has all valid keys, otherwise false
    """
    if len(listing) == 0:
        return True
    list_object = json.loads(listing)
    return not any(key not in listing_keys
                   for key in list_object)


def is_valid_integer_list(any_list):
    """
    Check if the complete list has all the integers or not.
    :param any_list:
    :return: true if all integers, otherwise false
    """
    list_object = json.loads(any_list)
    return not any(not is_valid_integer(str(listing_id)) for listing_id in
                   list_object)


def is_valid_email(email):
    """
    Checks is email is valid or not
    :param email: email that is needed to tested
    :return: True is email is valid

    """
    return validate_email(str(email))


def is_valid_province(province):
    """
    Checks the validity of a province string
    :param province: string that needs to be tested
    :return: true if valid province
    """
    return province.lower() in province_complete or province  in province_abbr


def is_valid_xor(dictionary, key1, key2):
    """
    Ensures both of the given keys are not in the dictionary.
    :param dictionary:
    :param key1:
    :param key2:
    :return:
    """
    if key1 in dictionary and key2 in dictionary:
        return is_empty(dictionary[key1]) or is_empty(dictionary[key2])
    else:
        return True


def is_valid_latitude(latitude):
    assert latitude is not None
    try:
        float(latitude)
        return -90 <= float(latitude) <= 90
        # return -90 <= latitude and latitude <= 90
    except ValueError:
        return False


def is_valid_postal_code(postal_code):
    # Postal code must be in the form A1A1A1 with no spaces in between
    # characters.
    assert postal_code is not None
    postal_code_re = re.compile(r"\s*(\w\d\s*){3}\s*")
    return postal_code_re.match(postal_code)


def is_valid_longitude(longitude):
    assert longitude is not None
    try:
        float(longitude)
        return -180 <= float(longitude) <= 180
        # return -180 <= longitude and longitude <= 180
    except ValueError:
        return False


def is_empty(var):
    """
    :param var:
    :return: True if the var is empty, false otherwise
    """
    return var in ["", u'', '', None, [], {}] or str(var).isspace()


# def is_valid_filter(filter):
#     if any(key not in ["sqft", "bedrooms", "bathrooms", "price", "city",
#                        "province", "address", "description", "isPublished", "images",
#                        "thumbnailImageIndex"] for key in filter):
#         return False
#     for key in filter:
#         if key in ["bedrooms", "bathrooms", "sqft", "price"]:
#             if any(bound not in ["lower", "upper"] for bound in key):
#                 return False


def is_valid_images(images):
    try:
        json.loads(images)
    except ValueError:
        return False
    return True


def convert_to_bool(input_string):
    """
    :param input_string: the string that needs to be converted to a boolean value
    :return: True if the var is in the list, false otherwise
    """

    return True if input_string in ['true', "True", "TRUE", '1', "t", "y", "yes"] else False


def is_existing_and_non_empty(existing_string, values):
    """
    :param existing_string: key string that need to check in the dictionary
    :param values: the dictionary
    :return: True if there's non-empty value for the key, false otherwise
    """
    return existing_string in values and not is_empty(values[existing_string])


def is_valid_read_del(read_del):
    if read_del is None:
        return False
    return read_del in ["r", "d", "R", "D" ]

"""
This dictionary is used to make checking for valid keys simpler. It maps the key
to it's validator.
"""

valid_check = {
    "phone1": is_valid_phone,
    "phone2": is_valid_phone,
    "email": is_valid_email,
    "password": is_valid_password,
    "province": is_valid_province,
    "userId": is_valid_integer,
    "listingId": is_valid_integer,
    "price": is_valid_integer,
    "bathrooms": is_valid_bathroom,
    "bedrooms": is_valid_integer,
    "squarefeet": is_valid_integer,
    "isPublished": is_valid_bool,
    "thumbnailImageIndex": is_valid_integer,
    "liked": is_valid_bool,
    "valuesRequired": is_valid_string_listing,
    "maxLimit": is_valid_integer,
    "listingIdList": is_valid_integer_list,
    "lower": is_valid_integer,
    "upper": is_valid_integer,
    "images": is_valid_images,
    "latitude": is_valid_latitude,
    "longitude": is_valid_longitude,
    "postalCode": is_valid_postal_code,
    "messageId": is_valid_integer,
    "readDel": is_valid_read_del,
    "fbId": is_valid_integer,
    "senderId": is_valid_integer,
    "receiverId": is_valid_integer
}


def write_error_to_response(response, error_dict, error_status):
    """
    Converts an error dict to json, and writes it to response.

    :param response: response object, where message needs to be written
    :param error_dict: the error message to be sent
    :param error_status: Error status, eg: 200 for success
    :return Nothing
    """
    response.write(json.dumps(error_dict))
    response.set_status(error_status)


def write_success_to_response(response, success_dict):
    """
    Converts dict to json, and writes it to response.
    This function should be used for successful calls.

    :param response: response object, where message needs to be written
    :param success_dict:
    :return:
    """
    response.write(json.dumps(success_dict))
    response.set_status(success)


def scale_province(province):
    """
    Scale the province to it's abbreviated form.
    :param province: valid province
    :return:
    """
    assert is_valid_province(province)
    if province.lower() in province_complete:
        province = province_abbr[province_complete.index(province.lower())]
    return province


def are_two_lists_same(list1, list2):
    """
    Checks if two lists are same
    :param list1: first list
    :param list2: second list
    :return: true if lists are identical
    """
    return len(set(list1).difference(set(list2))) == 0 and \
           len(list1) == len(list2)


def setup_testbed(test_handler):
    test_handler.testbed = testbed.Testbed()
    test_handler.testbed.activate()
    test_handler.testbed.init_datastore_v3_stub()
    test_handler.testbed.init_memcache_stub()
    test_handler.testbed.init_mail_stub()
    test_handler.mail_stub = test_handler.testbed.get_stub(testbed.MAIL_SERVICE_NAME)


def get_response_from_post(main, post, api):
    request = webapp2.Request.blank('/' + api,POST=post)
    response = request.get_response(main.app)
    if response.body:
        json_body = json.loads(response.body)
        if json_body:
            dictionary = {str(key): json_body[str(key)] for key in
                          json_body}
            return dictionary, response.status_int
    return None, response.status_int


def check_output_for_sign_in(self,output, database_user):
    """
    This function will assert false if the signed in user does not match
    the original user information.
    :param output: The output user dict to be checked
    :param database_user: The originally generated user dict
    """

    self.assertTrue('authToken' in output)
    self.assertTrue('userId' in output)
    user_saved = User.get_by_id(int(output['userId']))
    self.assertEquals(user_saved.first_name, database_user['firstName'])
    self.assertEquals(user_saved.last_name, database_user['lastName'])
    self.assertEquals(user_saved.city, database_user['city'])
    self.assertEquals(user_saved.email, database_user['email'])
    self.assertEquals(user_saved.phone1, database_user['phone1'])
    self.assertEquals(user_saved.phone2, database_user['phone2'])
    self.assertEquals(user_saved.province, database_user['province'])


def get_keys_from_values(values):
    return [str(x) for x in values]


def setup_post(response):
    response.headers.add_header('Access-Control-Allow-Origin', '*')


def setup_api_options(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = \
        'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
