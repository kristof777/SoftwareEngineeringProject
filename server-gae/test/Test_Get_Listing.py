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


    def test_get_listings(self):

        #######################################################################3
        # test case 1:

        valuesRequired = ["bedrooms", "bathrooms", "address"]
        maxLimit = 8
        listingIdList = [self.listings[0]['listingId'],
                         self.listings[1]['listingId'],
                         self.listings[2]['listingId'],
                         self.listings[3]['listingId'],
                         self.listings[4]['listingId'],
                         self.listings[5]['listingId'],
                         self.listings[6]['listingId']]


        get_listings = {
            "valuesRequired": ["bedrooms", "bathrooms", "address"],
            "maxLimit": 8,
            "listingIdList": [self.listings[0]['listingId'],
                              self.listings[1]['listingId']]
                              # self.listings[2]['listingId']
                              # self.listings[3]['listingId'],
                              # self.listings[4]['listingId'],
                              # self.listings[5]['listingId'],
                              # self.listings[6]['listingId']]
        }

        request = webapp2.Request.blank('/getListings', POST=get_listings)
        response = request.get_response(Main.app)
        print json.loads(response.body)
        print response.status_int
