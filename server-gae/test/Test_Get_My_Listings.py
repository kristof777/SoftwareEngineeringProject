from __future__ import absolute_import

import os
import unittest

import Main
import extras.Error_Code as Error_Code
from web_apis.Create_User import *
from API_NAME import *
from extras.Utils import get_response_from_post
from extras.Check_Invalid import *

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
        self.ownerToken = users[0]['authToken']

    def test_success_info(self):
        get_my_listings = {
            "userId": self.ownerId,
            "authToken": self.ownerToken
        }
        output, status_int = get_my_listing_api_response(get_my_listings)
        self.assertEquals(status_int, success)
        self.assertEquals(len(output["listings"]), 10)


    def test_invalid_userid(self):
        invalid_my_listings = {
            "userId": "blablabla",
            "authToken": self.ownerToken
        }

        response, status_int = get_my_listing_api_response(invalid_my_listings)

        self.assertEquals(status_int, missing_invalid_parameter)

        errors_expected = [Error_Code.invalid_user_id['error']]

        # checking if there is a difference between error_keys and what we got
        self.assertTrue(are_two_lists_same(errors_expected, response.keys()))


def get_my_listing_api_response(post):
    return get_response_from_post(Main, post, get_my_listings_api)
