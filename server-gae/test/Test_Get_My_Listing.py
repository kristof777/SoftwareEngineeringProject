from __future__ import absolute_import

import os
import unittest

import Main
import extras.Error_Code as Error_Code
from web_apis.Create_User import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestGetMyListing(unittest.TestCase):
    """
        test case 1: successful get info
        test case 2: invalid userId
    """

    def setUp(self):
        setup_testbed(self)

        # create 10 listings for one user
        self.listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(self.listings) == 10
        self.ownerId = users[0]['userId']
        self.ownerToken = users[0]['token']

    def test_success_info(self):
        get_my_listings = {
            "userId": self.ownerId,
            "authToken": self.ownerToken
        }

        request = webapp2.Request.blank('/getMyListings', POST=get_my_listings)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        output = json.loads(response.body)
        self.assertEquals(len(output["listings"]), 10)

    def test_invalid_userid(self):
        invalid_my_listings = {
            "userId": "blablabla",
            "authToken": self.ownerToken
        }

        request = webapp2.Request.blank('/getMyListings',
                                        POST=invalid_my_listings)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [Error_Code.invalid_user_id['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)




