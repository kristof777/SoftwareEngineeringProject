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
from extras.utils import create_random_user, are_two_lists_same
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
        inpput6: password not matching confirmedPassword
        input7: Everything valid
        :return:
        """

        input1 = {
            "email": "  ",
            "lastName": ""
        }  # Json object you need to send
        request = webapp2.Request.blank('/createUser', POST=input1)  # api you need to test
        response = request.get_response(Main.app)  # get response back
        # unit testing example checking if status is what we expected

        # test case 1
        # checking if all error codes are received, if empty code is sent

        self.assertEquals(response.status_int, 400)

        errors_expected = [missing_province['error'],
                           missing_confirmed_password['error'],
                           missing_password['error'],
                           missing_phone_number['error'],
                           missing_first_name['error'],
                           missing_city['error'],
                           missing_email['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got

        self.assertEquals(are_two_lists_same(error_keys,errors_expected ), True)

        #test 2 with invalid phone 1
        input2 = create_random_user()
        input2['phone1'] = "123456"
        request = webapp2.Request.blank('/createUser', POST=input2)  #   api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(invalid_phone1['error'], errors_expected)

        # test case 3 with phone2 invalid

        input3 = create_random_user()
        input3['phone2'] = "123456"
        request = webapp2.Request.blank('/createUser', POST=input3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)

        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(invalid_phone2['error'], errors_expected)

        # test case 4 invalid email

        input4 = create_random_user()
        input4['email'] = "gaa"
        request = webapp2.Request.blank('/createUser',
                                        POST=input4)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)

        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(invalid_email['error'], errors_expected)

        # test case 5 strong password

        input5 = create_random_user()
        input5['password'] = "123456"
        input5['confirmedPassword'] = "123456"
        request = webapp2.Request.blank('/createUser',
                                        POST=input5)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(password_not_strong['error'], errors_expected)


        # test case 6 password mismatch with confirmed password

        input6 = create_random_user()
        input6['password'] = "123456"
        request = webapp2.Request.blank('/createUser',
                                        POST=input6)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(password_not_strong['error'], errors_expected)

        # test case 7 correct information

        input7 = create_random_user()
        request = webapp2.Request.blank('/createUser', POST=input7)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        self.assertTrue("token" in output)
        self.assertTrue("userId" in output)
        user_saved = User.get_by_id(int(output["userId"]))
        self.assertEquals(user_saved.first_name,input7["firstName"])
        self.assertEquals(user_saved.last_name,input7["lastName"])
        self.assertEquals(user_saved.city,input7["city"])
        self.assertEquals(user_saved.email,input7["email"])
        self.assertEquals(user_saved.phone1,input7["phone1"])
        self.assertEquals(user_saved.province,input7["province"])






    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
