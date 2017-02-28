from __future__ import absolute_import
import unittest
import json
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import extras.Error_Code as Error_Code
import Main
import webapp2
from google.appengine.ext import testbed
from models.Listing import Listing
from web_apis.Create_User import *
import extras.utils as utils


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

        # create 10 listings for one user
        self.listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(self.listings) == 10
        self.ownerId = users[0]['userId']


    def test_get_my_listings(self):

        #######################################################################3
        # test case 1: successful get info

        get_my_listings = {
            "userId": self.ownerId
        }

        request = webapp2.Request.blank('/getMyListing', POST=get_my_listings)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        output = json.loads(response.body)
        self.assertEquals(len(output["myListings"]), 10)

        #######################################################################3
        # test case 2: invalid userId

        invalid_my_listings = {
            "userId": "blablabla"
        }

        request = webapp2.Request.blank('/getMyListing', POST=invalid_my_listings)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter_error)

        errors_expected = [Error_Code.invalid_user_id['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

