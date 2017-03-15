from __future__ import absolute_import

import json
import os
import sys

sys.path.append('../')
import unittest
from extras.Error_Code import *
import Main
import webapp2
from models.User import *
from extras.utils import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

class TestHandlerSignIn(unittest.TestCase):
    # Set up the testbeddegod7642q5

    def setUp(self):
        setup_testbed(self)
        self.database_entry = self.database_user = create_random_user()

        request = webapp2.Request.blank('/createUser', POST=self.database_entry)
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
        input2 = {'userId': self.user_id,
                  'authToken': 'ThisTokenIsNoGood'}
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
        input2 = {'userId': 'thisIsWrongId',
                  'authToken': self.token}
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
        input3 = {'userId': self.user_id,
                  'authToken': self.token}
        request = webapp2.Request.blank('/signInWithToken', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        # Check output
        output = json.loads(response.body)
        self.assertNotEqual(output['authToken'], self.token)
        check_output_for_sign_in(self,output,self.database_user)

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
