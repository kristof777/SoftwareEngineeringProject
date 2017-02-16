import unittest
import webapp2
import os
import main
import json
import error_code
from models.user import User
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
                  "password": "123456",
                  "firstName": "Student",
                  "lastName": "USASK",
                  "city": "Saskatoon",
                  "postalCode": "S7N 4P7",
                  "province": "Saskatchewan",
                  "phone1": 1111111111,
                  "confirmedPassword": "123456" }

        request = webapp2.Request.blank('/createuser', POST=database_entry1)
        response = request.get_response(main.app)
        #If this fails then create user unit tests should be run
        self.assertEquals(response.status_int, 200)

        input1 = {}  # Json object to send
        request = webapp2.Request.blank('/signin', POST=input1)  # api you need to test
        response = request.get_response(main.app)  # get response back
        # unit testing example checking if status is what we expected
        # test case 1
        # checking if all error codes are received, if empty code is sent
        self.assertEquals(response.status_int, 400)

        errors_expected = [error_code.missing_password['error'],
                           error_code.missing_email['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        input2 = {"email": "student@usask.ca",
                  "password": "notRighpassword123" }

        request = webapp2.Request.blank('/signin', POST=input2)  #   api you need to test
        response = request.get_response(main.app)
        self.assertEquals(response.status_int, 400)
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(error_code.password_mismatch['error'], errors_expected)

        # test case 3

        input2 = {"email": "student@usask.ca",
                  "password": "123456" }

        request = webapp2.Request.blank('/signin', POST=input2)  #   api you need to test
        response = request.get_response(main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        self.assertTrue("token" in output)
        self.assertTrue("userId" in output)
        user_saved = User.get_by_id(int(output["userId"]))
        self.assertEquals(user_saved.first_name,"Student")
        self.assertEquals(user_saved.last_name,"USASK")
        self.assertEquals(user_saved.city,"Saskatoon")
        self.assertEquals(user_saved.postal_code,"S7N 4P7")
        self.assertEquals(user_saved.email,"student@usask.ca")
        self.assertEquals(int(user_saved.phone1),1111111111)
        self.assertEquals(user_saved.province,"Saskatchewan")






    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
