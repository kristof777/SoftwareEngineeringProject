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


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate() 
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.user_buyer = create_dummy_users_for_testing(1, Main)
        self.user_seller, self.listing = create_dummy_listings_for_testing(Main,
                                                                           1)


    def test_sign_out(self):
        """
        # Test1: User signed in with email
        # Test2: User signed in with token
        :return:
        """

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def get_post_dictionary(user_id, token, listing_id, message, phone1, phone2, ):
    return {"userId": user_id, "authToken":token,"changeValues": json.dumps(change_values)}


def get_response(POST):
    request = webapp2.Request.blank('/editUser', POST=POST)
    response = request.get_response(Main.app)
    return json.loads(response.body), response.status_int




def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
