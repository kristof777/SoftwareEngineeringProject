from __future__ import absolute_import
import sys
from extras.Error_Code import *
sys.path.append("../")
import os
import unittest
import Main
from extras.utils import get_response_from_post
from API_NAME import *


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.utils import *


class TestHandlerChangePassword(unittest.TestCase):
    def setUp(self):
        setup_testbed(self)
        # I need to create the database entry manually because I need access
        # to the password.
        self.database_user = create_random_user()
        self.database_user['password'] = 'aaAA1234'
        self.database_user['confirmedPassword'] = 'aaAA1234'
        self.database_user['email'] = 'student@usask.ca'

        request = webapp2.Request.blank('/createUser', POST=self.database_user)
        response = request.get_response(Main.app)

        self.user = json.loads(response.body)
        self.assertTrue("userId" in self.user)
        self.user_id = self.user['userId']

        # If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, success)

    def test_change_password(self):
        # Test Case: Success case
        input = {"oldPassword": "aaAA1234",
                  "newPassword": "newPass123",
                  "confirmedPassword": "newPass123",
                  "userId": self.user_id}
        request = webapp2.Request.blank('/changePassword', POST=input)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        output = json.loads(response.body)
        self.assertTrue("authToken" in output)

        #Check to make sure old password no longer works
        input2 = {'email': 'student@usask.ca',
                  'password': 'aaAA1234'}
        request = webapp2.Request.blank('/signIn', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys[0], not_authorized['error']))


    def test_missing_fields(self):
        # Test case: One or more fields were not entered
        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/changePassword', POST=input1)
        response = request.get_response(Main.app)  # get response back

        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [missing_password['error'],
                           missing_new_password['error'],
                           missing_confirmed_password['error'],
                           missing_user_id['error']]
        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

    def test_incorrect_old_pass(self):
        # Case 2: Incorrect old password
        input2 = {"oldPassword": "Wrongpassword123",
                  "newPassword": "notImportant123",
                  "confirmedPassword": "notImportant123",
                  "userId": self.user_id}

        request = webapp2.Request.blank('/changePassword', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
            return
        self.assertEquals(not_authorized['error'], error_message)

    def test_missmatched_passwords(self):
        # Case3: Passwords do not match
        input3 = {"oldPassword": "aaAA1234",
                  "newPassword": "NotMatching123",
                  "confirmedPassword": "doesntMatch123",
                  "userId": self.user_id}

        request = webapp2.Request.blank('/changePassword', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, unauthorized_access)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
        self.assertEquals(password_mismatch['error'], error_message)

    def test_weak_passwords(self):
        # Case4: new passwords match but are not strong
        input4 = {"oldPassword": "aaAA1234",
                  "newPassword": "weakmatch",
                  "confirmedPassword": "weakmatch",
                  "userId": self.user_id}

        request = webapp2.Request.blank('/changePassword', POST=input4)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
        self.assertEquals(password_not_strong['error'], error_message)

    def test_change_to_same_password(self):
        # Case5: new passwords and old password are the same
        input4 = {"oldPassword": "aaAA1234",
                  "newPassword": "aaAA1234",
                  "confirmedPassword": "aaAA1234",
                  "userId": self.user_id}

        request = webapp2.Request.blank('/changePassword', POST=input4)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse(True)
        self.assertEquals(new_password_is_the_same_as_old['error'],
                          error_message)




    def tearDown(self):
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
