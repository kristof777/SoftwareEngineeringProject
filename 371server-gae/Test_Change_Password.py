import json
import os
import unittest
import Error_Code
import Main
import webapp2
from google.appengine.ext import testbed

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlerSignIn(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which will allow you to use
        # service stubs.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
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

        #Case 1: User is not signed in
        #TODO

        #Case 2: They do not enter one or many fields.

        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/changepassword', POST=input1)
        response = request.get_response(Main.app)  # get response back

        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.missing_password['error'],
                           Error_Code.missing_new_password['error'],
                           Error_Code.missing_new_password_confirmed['error']]
        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #Case 3: Incorrect current password
        input2 = {"oldpassword": "Wrongpassword123",
                  "newpassword": "notImportant123",
                  "confirmedpassword": "notImportant123"}

        request = webapp2.Request.blank('/changepassword', POST=input2)  #   api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 401)
        try:
            error_message = str(json.loads(response.body))
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(Error_Code.not_authorized['error'], error_message)

        input2 = {"oldpassword": "AAaa1234",
                  "password": "AAaa1234" }

        request = webapp2.Request.blank('/signin', POST=input2)  #   api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        #Case4: Invalid Password

        #Case5: Passwords do not match

        #Case6: Success


    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
