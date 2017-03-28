from __future__ import absolute_import

import os
import unittest

import Main
import extras.Error_Code as Error_Code
from web_apis.Create_User import *
from extras.Utils import get_response_from_post
from API_NAME import *
from extras.Check_Invalid import *
from extras.Random_Models import *
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestGetFavouriteListing(unittest.TestCase):
    """
    Test case 1: successful get info
    Test case 2: Invalid userId
    """
    def setUp(self):
        setup_testbed(self)

        # create 10 listings for one user
        listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(listings) == 10

        # now create a new user as a liker, we'll use this person to send GetFavourites request
        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        liker = users[0]
        self.likerId = liker['userId']
        self.likerToken = liker['authToken']

        # make the liker likes the first five of the listings

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[0]['listingId'],
                                                                       self.likerToken,  "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[1]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[2]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[3]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[4]['listingId'],
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        # the first five listings has been liked, so we create a list of those listings for future use
        self.likedListings = listings[0:5]


    def test_success(self):

        get_favs = {
            "userId": self.likerId,
            "authToken": self.likerToken
        }
        output, response_status = get_favourites_response(get_favs)
        self.assertEquals(response_status, success)
        # get the number of published listings
        is_published = 0
        for listing in self.likedListings:
            if listing['isPublished'] == 'True':
                is_published += 1
        self.assertEquals(len(output["listings"]), is_published)

    def test_invalid_userid(self):
        invalid_favs = {
            "userId": "blablabla",
            "authToken": self.likerToken
        }
        response, response_status = get_favourites_response(invalid_favs)
        self.assertEquals(response_status, missing_invalid_parameter)
        errors_expected = [Error_Code.invalid_user_id['error']]
        # checking if there is a difference between error_keys and what we got
        self.assertTrue(are_two_lists_same(errors_expected, response.keys()))


    def tearDown(self):
        self.testbed.deactivate()


def get_like_post_dictionary(user_id, listing_id, authToken, liked):
    return {"userId": user_id, "listingId": listing_id,
            "authToken": authToken, "liked": liked}


def get_like_response(post):
    return get_response_from_post(Main, post, like_listing_api)


def get_favourites_response(post):
    return get_response_from_post(Main, post, get_favourites_listing_api)
