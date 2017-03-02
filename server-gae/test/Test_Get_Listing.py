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
        self.listings, users = create_dummy_listings_for_testing(Main, 20)
        assert len(users) == 1
        assert len(self.listings) == 20
        self.ownerId = users[0]['userId']

        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        self.userId = users[0]['userId']

        # make the user like a few listings
        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[0]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[1]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[2]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[3]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.userId, self.listings[4]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

    def test_get_listings(self):
        #######################################################################3
        # test case 1: empty input, only return listingIds

        get_filter_listings = {}

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        self.assertEquals(len(res_value), len(self.listings))
        for value in res_value:
            self.assertTrue("listingId" in value)
        #######################################################################3
        # test case 2: empty filer and valuesRequired, only return listingIds

        get_filter_listings = {
            "valuesRequired": "",
            "filter": ""
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        self.assertEquals(len(res_value), len(self.listings))
        for value in res_value:
            self.assertTrue("listingId" in value)
        #######################################################################3
        # test case 3: unrecognized key in filter

        get_filter_listings = {
            "valuesRequired":"",
            "userId": "",
            "filter": ""
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        self.assertEquals(len(res_value), len(self.listings))
        for value in res_value:
            self.assertTrue("listingId" in value)

        #######################################################################3
        # test case 4: unrecognized key in filter

        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "filter": json.dumps({
                "price": {
                    "lower": 100,
                    "upper": 8000000,
                    "what": "is_this"
                },
                "bedrooms": {
                    "lower": 1,
                    "upper": 1000
                },
                "bathrooms": {
                    "lower": 1.0,
                    "upper": 200
                },
                "province": "Saskatchewan"
            })
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = invalid_filter_bound['error']

        self.assertTrue(error_expected in res_value)

        #######################################################################3
        # test case 5: unrecognized key in filter

        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "filter": json.dumps({
                "price": {
                    "lower": 100,
                    "upper": 8000000
                },
                "bedrooms": {
                    "lower": 1,
                    "upper": 1000
                },
                "bathrooms": {
                    "lower": 1.0,
                    "upper": 200
                },
                "province": "Saskatchewan",
                "what_the_heck": "is_this"
            })
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = unrecognized_key['error']

        self.assertTrue(error_expected in res_value)

        #######################################################################3
        # test case 6: get get listings with listingIdList

        get_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address"]),
            "maxLimit": 8,
            "listingIdList": json.dumps([self.listings[0]['listingId'],
                                         self.listings[1]['listingId'],
                                         self.listings[2]['listingId'],
                                         self.listings[3]['listingId'],
                                         self.listings[4]['listingId'],
                                         self.listings[5]['listingId'],
                                         self.listings[6]['listingId']])
        }

        res_value, status = get_listing_response(get_listings)
        self.assertEqual(status, success)
        self.assertEquals(len(res_value), 7)

        #######################################################################3
        # test case 7: get listings with filter and userid

        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price"]),
            "maxLimit": 8,
            "userId": self.userId,
            "filter": json.dumps({
                "price": {
                    "lower": 100,
                    "upper": 8000000
                },
                "bedrooms": {
                    "lower": 1,
                    "upper": 1000
                },
                "bathrooms": {
                    "lower": 1.0,
                    "upper": 200
                },
                "province": "Saskatchewan"
            })
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, success)
        for value in res_value:
            assert len(value) == 4
            assert int(value['price']) <= int(json.loads(get_filter_listings['filter'])['price']['upper'])
            assert int(value['price']) >= int(json.loads(get_filter_listings['filter'])['price']['lower'])
            assert int(value['bedrooms']) <= int(json.loads(get_filter_listings['filter'])['bedrooms']['upper'])
            assert int(value['bedrooms']) >= int(json.loads(get_filter_listings['filter'])['bedrooms']['lower'])
            assert float(value['bathrooms']) <= float(json.loads(get_filter_listings['filter'])['bathrooms']['upper'])
            assert float(value['bathrooms']) >= float(json.loads(get_filter_listings['filter'])['bathrooms']['lower'])

        #######################################################################3
        # test case 8: invalid key in valuesRequired

        get_filter_listings = {
            "valuesRequired": json.dumps(["bedrooms", "bathrooms", "address", "price", "what_the_heck"]),
        }

        res_value, status = get_listing_response(get_filter_listings)
        self.assertEqual(status, missing_invalid_parameter)
        error_expected = invalid_values_required['error']

        self.assertTrue(error_expected in res_value)


def get_like_post_dictionary(userId, listingId, liked):
    return {"userId": userId, "listingId":
        listingId, "liked": liked}


def get_like_response(POST):
    request = webapp2.Request.blank('/like', POST=POST)
    response = request.get_response(Main.app)
    if response.body:
        return json.loads(response.body), response.status_int
    else:
        return None, response.status_int


def get_listing_response(POST):
    request = webapp2.Request.blank('/getListings', POST=POST)
    response = request.get_response(Main.app)
    if response.body:
        return json.loads(response.body), response.status_int
    else:
        return None, response.status_int