from __future__ import absolute_import
import json
import os
import sys
sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from google.appengine.ext import testbed
from extras.utils import *
from models.User import User
import Main


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
        self.users = create_dummy_users_for_testing(10, Main)

    def test_edit_user(self):
        """
        Test case 1: email already exists
        Test case 2: nothing requested to change
        Test case 3: unrecognized key
        Test case 4: invalid userId
        Test case 5: missing userId
        Test case 6: password can't be changed
        Test case 7: 1 item changed
        Test case 8: 2 items changed
        Test case 9: many items changed
        """
        #Test case 2 : Nothing requested to change

        user_id = self.users[0]["userId"]
        token = self.users[0]["token"]
        change_values = {}

        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))

        self.assertEqual(status, missing_invalid_parameter_error)
        self.assertTrue(nothing_requested_to_change["error"] in res_value)

        #  Test case 3: unrecognized key

        change_values = {"unRecongnized" :"key"}

        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))

        self.assertEqual(status, unrecognized_key["status"])
        self.assertTrue(unrecognized_key["error"] in res_value)

        # Test case 4: invalid userId
        change_values = {"phone1" :"1234567891"}

        user_id = 1000

        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))
        self.assertEqual(status, not_authorized["status"])
        self.assertTrue(not_authorized["error"] in res_value)


        # Test case 5: missing userId

        user_id = ""
        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))
        self.assertEqual(status, missing_user_id["status"])
        self.assertTrue(missing_user_id["error"] in res_value)




        # Test case 6: password can't be changed

        user_id = self.users[0]["userId"]
        change_values = {"password" :"1234567891"}


        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))
        self.assertEqual(status, password_cant_be_changed["status"])
        self.assertTrue(password_cant_be_changed["error"] in res_value)


        # Test case 7: 1 item changed

        change_values = {"phone1": "1234567891"}

        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))
        self.assertEqual(status, success)

        new_user = User.get_by_id(int(self.users[0]["userId"]))
        self.assertEqual(new_user.phone1, change_values["phone1"])

        # Test case 8: 2 items changed

        user_id = self.users[1]["userId"]
        token = self.users[1]["token"]
        change_values = {"phone1": "1234567891", "firstName": "Hello"}
        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))
        self.assertEqual(status, success)

        new_user = User.get_by_id(int(self.users[1]["userId"]))
        self.assertEqual(new_user.phone1, change_values["phone1"])
        self.assertEqual(new_user.first_name, change_values["firstName"])

        # Test case 9: many items changed

        user_id = self.users[2]["userId"]
        token = self.users[2]["token"]
        change_values = {"phone1": "1234567891", "firstName": "hello",
                         "lastName": "world"}
        res_value, status = get_response(get_post_dictionary(user_id, token,
                                                             change_values))
        self.assertEqual(status, success)
        new_user = User.get_by_id(int(self.users[2]["userId"]))
        self.assertEqual(new_user.phone1, change_values["phone1"])
        self.assertEqual(new_user.last_name, change_values["lastName"])













    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def get_post_dictionary(userId, token, change_values):
    return {"userId": userId, "authToken":
        token,"changeValues": json.dumps(change_values)}


def get_response(POST):
    request = webapp2.Request.blank('/editUser', POST=POST)
    response = request.get_response(Main.app)
    return json.loads(response.body), response.status_int




def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
