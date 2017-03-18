from __future__ import absolute_import

import os
import sys

sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *


class TestSignOut(unittest.TestCase):
    def setUp(self):
        setup_testbed(self)
        self.users = create_dummy_users_for_testing(Main, 1)

    def test_sign_out(self):
        """
        # Test1: User signed in with email
        # Test2: User signed in with token
        :return:
        """
        pass

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

