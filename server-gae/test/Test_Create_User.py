from __future__ import absolute_import
import json
import os
import sys
sys.path.append("../")
import unittest
from extras.Error_Code import *
import Main
import webapp2
from google.appengine.ext import testbed
from models.User import User
from extras.utils import create_random_user
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlers(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which will allow you to use
        # service stubs.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    def test_create_user(self):
        """
        input1: different kinds of empty strings and Null values
        input2: invalid phone number 1
        input3: invalid phone number 2
        input4: invalid email
        input5: not strong password
        input6: Everything valid
        :return:
        """


        input1 = {
            "email" : "  ",
            "lastName": ""
        }  # Json object you need to send
        request = webapp2.Request.blank('/createuser', POST=input1)  # api you need to test
        response = request.get_response(Main.app)  # get response back
        # unit testing example checking if status is what we expected
        # test case 1
        # checking if all error codes are received, if empty code is sent
        self.assertEquals(response.status_int, 400)

        errors_expected = [missing_province['error'],
                           missing_confirmed_password['error'],
                           missing_password['error'],
                           missing_last_name['error'],
                           missing_phone_number['error'],
                           missing_first_name['error'],
                           missing_city['error'],
                           missing_email['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        print(error_keys)
        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        input2 = create_random_user()
        input2['password'] = "123456"
        request = webapp2.Request.blank('/createuser', POST=input2)  #   api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(Error_Code.password_mismatch['error'], errors_expected)

        # test case 3 without strong password

        input3 = {"email": "student@usask.ca",
                  "password": "123456",
                  "firstName": "Student",
                  "lastName": "USASK",
                  "city": "Saskatoon",
                  "province": "Saskatchewan",
                  "phone1": 1111111111,
                  "confirmedPassword": "123456"
                  }

        request = webapp2.Request.blank('/createuser', POST=input2)  #   api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)

        # test case 4 without strong password

        input3 = {"email": "student@usask.ca",
                  "password": "ABab1234",
                  "firstName": "Student",
                  "lastName": "USASK",
                  "city": "Saskatoon",
                  "postalCode": "S7N 4P7",
                  "province": "Saskatchewan",
                  "phone1": 1111111111,
                  "confirmedPassword": "ABab1234"
                  }

        request = webapp2.Request.blank('/createuser',
                                        POST=input3)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        self.assertTrue("token" in output)
        self.assertTrue("userId" in output)
        user_saved = User.get_by_id(int(output["userId"]))
        self.assertEquals(user_saved.first_name,"Student")
        self.assertEquals(user_saved.last_name,"USASK")
        self.assertEquals(user_saved.city,"Saskatoon")
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
