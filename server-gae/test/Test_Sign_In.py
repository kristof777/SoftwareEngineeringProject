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
    def setUp(self):
        setup_testbed(self)
        self.database_user = create_random_user()
        # explicitly set the email to this so that we can test case sensitivity
        self.database_user['email'] = 'student@usask.ca'
        request = webapp2.Request.blank('/createUser', POST=self.database_user)
        response = request.get_response(Main.app)
        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, success)

    def test_sign_in(self):

        # Test with correct e-mail and password
        input3 = {'email': 'student@usask.ca',
                  'password': self.database_user['password']}

        request = webapp2.Request.blank('/signIn', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)

        #Check output
        output = json.loads(response.body)
        check_output_for_sign_in(self, json.loads(response.body), self.database_user)

    def test_sign_in_uppercase_email(self):
        # Test with correct e-mail and password, but email is capitalized.
        input3 = {'email': 'STUDENT@usask.ca',
                  'password': self.database_user['password']}

        request = webapp2.Request.blank('/signIn', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        check_output_for_sign_in(self,json.loads(response.body), self.database_user)

    def test_no_params(self):
        # Test1: when no paramaters are given
        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/signIn', POST=input1)
        response = request.get_response(Main.app)  # get response back
        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [missing_password['error'],
                           missing_email['error']]
        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

    def test_incorrect_password(self):
        # Test2: When incorrect password is entered
        input2 = {'email': 'student@usask.ca',
                  'password': self.database_user['password'] + 'wrongPassword'}
        request = webapp2.Request.blank('/signIn', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(not_authorized['error'], error_message)

    def test_incorrect_userName(self):
        # Test2: When incorrect user_name, but correct password
        input2 = {'email': 'WrongEmail.com',
                  'password': 'aaAA1234'}
        request = webapp2.Request.blank('/signIn', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(not_authorized['error'], error_message)




    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
