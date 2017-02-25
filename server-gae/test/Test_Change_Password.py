from __future__ import absolute_import
import sys
sys.path.append("../")
import json
import os
import unittest
import extras.Error_Code as Error_Code
import Main
import webapp2
from google.appengine.ext import testbed

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlerSignIn(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def test_sign_in(self):
        database_entry1 = {"email": "student@usask.ca",
                  "password": "aaAA1234",
                  "firstName": "Student",
                  "lastName": "USASK",
                  "city": "Saskatoon",
                  "postalCode": "S7N 4P7",
                  "province": "Saskatchewan",
                  "phone1": 1111111111,
                  "confirmedPassword": "aaAA1234" }

        request = webapp2.Request.blank('/createuser', POST=database_entry1)
        response = request.get_response(Main.app)
        #If this assert fails then create user unit tests should be run
        self.assertEquals(response.status_int, 200)


        #Case 1: They do not enter one or many fields.
        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/changepassword', POST=input1)
        response = request.get_response(Main.app)  # get response back

        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.missing_password['error'],
                           Error_Code.missing_new_password['error'],
                           Error_Code.missing_new_password_confirmed['error']]
        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #Case 2: Incorrect old password
        input2 = {"oldpassword": "Wrongpassword123",
                  "newpassword": "notImportant123",
                  "confirmedpassword": "notImportant123"}

        request = webapp2.Request.blank('/changepassword', POST=input2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 401)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(Error_Code.not_authorized['error'], error_message)

        #Case3: Passwords do not match
        input3 = {"oldpassword": "aaAA1234",
                  "newpassword": "NotMatching123",
                  "confirmedpassword": "doesntMatch123"}

        request = webapp2.Request.blank('/changepassword', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 403)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(Error_Code.password_mismatch['error'], error_message)

        #Case4: new passwords match but are not strong
        input4 = {"oldpassword": "aaAA1234",
                  "newpassword": "NotMatching123",
                  "confirmedpassword": "doesntMatch123"}

        request = webapp2.Request.blank('/changepassword', POST=input4)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 403)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()
        self.assertEquals(Error_Code.password_not_strong['error'], error_message)

        #Case5: Success case
        input5 = {"oldpassword": "aaAA1234",
                  "newpassword": "newPass123",
                  "confirmedpassword": "newPass123"}

        request = webapp2.Request.blank('/changepassword', POST=input5)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        output = json.loads(response.body)
        self.assertTrue("token" in output)


    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
