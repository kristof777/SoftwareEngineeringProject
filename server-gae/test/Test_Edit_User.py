from __future__ import absolute_import
import json
import os
import sys
sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import extras.Error_Code as Error_Code
import Main
import webapp2
from google.appengine.ext import testbed
from models.Listing import Listing
from web_apis.Create_User import *
from models.User import User


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
        self.users = create_dummy_users_for_testing(10)

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
        userId = self.users[0]["userId"]
        token = self.users[0]["token"]
        changeValues = json.dumps({"phone1":1111111111})

        request = webapp2.Request.blank('/editUser',POST={
            "userId": userId, "authToken": token, "changeValues":changeValues})
        response = request.get_response(Main.app)


    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()

def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
