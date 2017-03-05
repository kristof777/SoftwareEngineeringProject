from __future__ import absolute_import

import sys

from extras.Error_Code import *

sys.path.append("../")
import json
import os
import unittest
import Main
import webapp2

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.utils import setup_testbed  # TODO add newPassword=oldPassword


class TestHandlerChangePassword(unittest.TestCase):
    def setUp(self):
        setup_testbed(self)

    def test_change_password(self):
        database_entry1 = {"email": "student@usask.ca",  # TODO Random utils
                  "password": "aaAA1234",
                  "firstName": "Student",
                  "lastName": "USASK",
                  "city": "Saskatoon",
                  "postalCode": "S7N 4P7",
                  "province": "Saskatchewan",
                  "phone1": 1111111111,
                  "confirmedPassword": "aaAA1234" }

        request = webapp2.Request.blank('/createUser', POST=database_entry1)  # TODO make fn
        response = request.get_response(Main.app)

        user = json.loads(response.body)
        self.assertTrue("userId" in user)
        user_id = user['userId']

        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, 200)


        # Case 1: They do not enter one or many fields.
        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/changePassword', POST=input1)
        response = request.get_response(Main.app)  # get response back

        self.assertEquals(response.status_int, 400)
        errors_expected = [missing_password['error'],
                           missing_new_password['error'],
                           missing_confirmed_password['error'],
                           missing_user_id['error']]
        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertEquals(len(set(errors_expected).  # TODO use fn in utils
                              difference(set(error_keys))), 0)

        # Case 2: Incorrect old password
        input2 = {"oldPassword": "Wrongpassword123",
                  "newPassword": "notImportant123",
                  "confirmedPassword": "notImportant123",
                  "userId": user_id}

        request = webapp2.Request.blank('/changePassword', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 401)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
        self.assertEquals(not_authorized['error'], error_message)

        # Case3: Passwords do not match
        input3 = {"oldPassword": "aaAA1234",
                  "newPassword": "NotMatching123",
                  "confirmedPassword": "doesntMatch123",
                  "userId": user_id}

        request = webapp2.Request.blank('/changePassword', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 401)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
        self.assertEquals(password_mismatch['error'], error_message)

        # Case4: new passwords match but are not strong
        input4 = {"oldPassword": "aaAA1234",
                  "newPassword": "weakmatch",
                  "confirmedPassword": "weakmatch",
                  "userId": user_id}

        request = webapp2.Request.blank('/changePassword', POST=input4)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 403)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
        self.assertEquals(password_not_strong['error'], error_message)

        # Case5: Success case
        input5 = {"oldPassword": "aaAA1234",
                  "newPassword": "newPass123",
                  "confirmedPassword": "newPass123",
                  "userId": user_id}

        request = webapp2.Request.blank('/changePassword', POST=input5)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        output = json.loads(response.body)
        self.assertTrue("token" in output)


    def tearDown(self):
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
