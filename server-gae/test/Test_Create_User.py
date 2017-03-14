from __future__ import absolute_import
import json
import os
import sys
sys.path.append("../")
import unittest
from extras.Error_Code import *
import Main
import webapp2
from models.User import User
from models.FB import FBLogin
from extras.utils import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'




class TestCreateUser(unittest.TestCase):
    """
    These are test, being tested
    Different kinds of empty strings and null values
    Test invalid phone 1
    Test invalid phone 2
    Test password mismatch
    Test not strong password
    Test all valid fields
    """
    def setUp(self):
        setup_testbed(self)
        self.api = "createUser"

    def test_missing_fields(self):
        """
        Different kinds of empty strings and null values
        :return:
        """
        input = {
            "email": "  ",
            "lastName": ""
        }

        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [missing_province['error'],
                           missing_confirmed_password['error'],
                           missing_password['error'],
                           missing_phone_number['error'],
                           missing_first_name['error'],
                           missing_city['error'],
                           missing_email['error']]

        error_keys = [str(x) for x in response_body]
        self.assertEquals(are_two_lists_same(error_keys,errors_expected), True)

    def test_invalid_phone1(self):
        """
        Test invalid phone 1
        :return:
        """
        input = create_random_user()
        input['phone1'] = "123456"
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [invalid_phone1['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_invalid_phone2(self):
        input = create_random_user()
        input['phone2'] = "123456"
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [invalid_phone2['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_invalid_email(self):
        input = create_random_user()
        input['email'] = "gaa"
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [invalid_email['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_not_strong_password(self):
        input = create_random_user()
        input['password'] = "123456"
        input['confirmedPassword'] = "123456"
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [password_not_strong['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys), True)

    def test_password_mismatch(self):
        input = create_random_user()
        input['confirmedPassword'] = "123456"
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, missing_invalid_parameter)
        errors_expected = [password_mismatch['error']]
        error_keys = [str(x) for x in response_body]
        self.assertTrue(are_two_lists_same(errors_expected, error_keys))

    def test_create_user_without_fb(self):
        input = create_random_user()
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, success)
        self.assertTrue("token" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))
        self.assertEquals(user_saved.first_name,input["firstName"])
        self.assertEquals(user_saved.last_name,input["lastName"])
        self.assertEquals(user_saved.city,input["city"])
        self.assertEquals(user_saved.email,input["email"])
        self.assertEquals(user_saved.phone1,input["phone1"])
        self.assertEquals(user_saved.province,input["province"])

    def test_create_user_with_fb(self):
        input = create_random_user()
        input["fbId"] = "1212312398"
        response_body, status_int = get_response_from_post(Main, input,
                                                           self.api)
        self.assertEquals(status_int, success)
        self.assertTrue("token" in response_body)
        self.assertTrue("userId" in response_body)
        user_saved = User.get_by_id(int(response_body["userId"]))
        self.assertEquals(user_saved.first_name,input["firstName"])
        self.assertEquals(user_saved.last_name,input["lastName"])
        self.assertEquals(user_saved.city,input["city"])
        self.assertEquals(user_saved.email,input["email"])
        self.assertEquals(user_saved.phone1,input["phone1"])
        self.assertEquals(user_saved.province,input["province"])
        fb_e_id = FBLogin.query().fetch(keys_only=True)[0].integer_id()
        fb_e = FBLogin.get_by_id(fb_e_id)
        self.assertEquals(fb_e.user_id,int(response_body["userId"]))
        self.assertEquals(fb_e.fb_id, int(input["fbId"]))








    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




# suite = unittest.TestLoader().loadTestsFromTestCase(TestHandlers)
# unittest.TextTestRunner(verbosity=3).run(suite)
