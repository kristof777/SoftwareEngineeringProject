from __future__ import absolute_import

import json
import os
import sys

sys.path.append('../')
import unittest
import extras.Error_Code as Error_Code
import Main
import webapp2
from models.User import *
from extras.utils import setup_testbed
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# TODO Add case to check case insensitive email
class TestHandlerSignIn(unittest.TestCase):
    # TODO explain all test cases handled
    def setUp(self):
        setup_testbed(self)


    def test_sign_in(self):
        database_entry1 = {'email': 'student@usask.ca',
                           'password': 'aaAA1234',
                           'firstName': 'Student',
                           'lastName': 'USASK',
                           'city': 'Saskatoon',
                           'postalCode': 'S7N 4P7',
                           'province': 'Saskatchewan',
                           'phone1': '1111111111',
                           'confirmedPassword': 'aaAA1234'}

        request = webapp2.Request.blank('/createUser', POST=database_entry1)
        response = request.get_response(Main.app)
        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, 200) # TODO Use enums

        # Test1: when no paramaters are given
        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/signIn', POST=input1)
        response = request.get_response(Main.app)  # get response back
        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.missing_password['error'],
                           Error_Code.missing_email['error']]
        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)  # TODO use fn from utils to compare lists

        # Test2: When incorrect password is entered
        input2 = {'email': 'student@usask.ca',
                  'password': 'notRighpassword123'} # TODO make password invalid
        request = webapp2.Request.blank('/signIn', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 401)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(Error_Code.not_authorized['error'], error_message)

        # Test3: with correct e-mail and password
        input3 = {'email': 'student@usask.ca',
                  'password': 'aaAA1234'}

        request = webapp2.Request.blank('/signIn', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        #Check output
        output = json.loads(response.body)
        self.assertTrue('token' in output)
        self.assertTrue('userId' in output)
        user_saved = User.get_by_id(int(output['userId']))
        self.assertEquals(user_saved.first_name, 'Student')
        self.assertEquals(user_saved.last_name, 'USASK')
        self.assertEquals(user_saved.city, 'Saskatoon')
        self.assertEquals(user_saved.email, 'student@usask.ca')
        self.assertEquals(int(user_saved.phone1), 1111111111)
        self.assertEquals(user_saved.province, 'SK')



    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
