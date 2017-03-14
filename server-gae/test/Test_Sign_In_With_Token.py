from __future__ import absolute_import

import json
import os
import sys

sys.path.append("../")
import unittest
from extras.Error_Code import *
import Main
import webapp2
from models.User import *
from extras.utils import setup_testbed

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlerSignIn(unittest.TestCase):
    # Set up the testbeddegod7642q5

    def setUp(self):
        setup_testbed(self)
        database_entry1 = {"email": "student@usask.ca",
                           "password": "aaAA1234",
                           "firstName": "Student",
                           "lastName": "USASK",
                           "city": "Saskatoon",
                           "postalCode": "S7N 4P7",
                           "province": "Saskatchewan",
                           "phone1": "1111111111",
                           "confirmedPassword": "aaAA1234"}

        request = webapp2.Request.blank('/createUser', POST=database_entry1)
        response = request.get_response(Main.app)
        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, success)
        self.user_id = json.loads(response.body)['userId']
        self.token = json.loads(response.body)['authToken']

    def test_sign_in_missing_params(self):
        # No input parameters
        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/signInWithToken', POST=input1)
        response = request.get_response(Main.app)  # get response back
        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [missing_user_id['error'],
                           missing_token['error']]
        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

    def test_sign_in_incorrect_token(self):
        # Test2: When incorrect token
        input2 = {"userId": self.user_id,
                  "authToken": "ThisTokenIsNoGood"}
        request = webapp2.Request.blank('/signInWithToken', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(not_authorized['error'], error_message)

    def test_sign_in_incorrect_user_id(self):
        # Test2: When incorrect user_id
        input2 = {"userId": "thisIsWrongId",
                  "authToken": self.token}
        request = webapp2.Request.blank('/signInWithToken', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(not_authorized['error'], error_message)

    def test_sign_in_success(self):
        # Correct user_id and authToken
        input3 = {"userId": self.user_id,
                  "authToken": self.token}
        request = webapp2.Request.blank('/signInWithToken', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        # Check output
        output = json.loads(response.body)
        self.assertTrue("authToken" in output)
        self.assertTrue("userId" in output)
        # should be a different token.
        self.assertNotEqual(output['authToken'], self.token)
        user_saved = User.get_by_id(int(output["userId"]))
        self.assertEquals(user_saved.first_name, "Student")
        self.assertEquals(user_saved.last_name, "USASK")
        self.assertEquals(user_saved.city, "Saskatoon")
        self.assertEquals(user_saved.email, "student@usask.ca")
        self.assertEquals(int(user_saved.phone1), 1111111111)
        self.assertEquals(user_saved.province, "SK")

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
