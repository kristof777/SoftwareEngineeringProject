from __future__ import absolute_import

import sys
import unittest

import Main
from web_apis.Like_Dislike_Listing import *

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestLikeListingApi(unittest.TestCase):
    """
        test case 1: the owner can't like their listings
        now user want to like the listing
        test case 2: successful delivery (like the listing)
        test case 3: send a like request(liked==True) while the listing is already liked
        test case 4: dislike this listing
        should be a successful delivery
        test case 5: dislike this listing again
        test case 6: missing user input
        test case 7: invalid user input
    """
    def setUp(self):
        setup_testbed(self)

        # create a user as well as a listing that the user owns
        listings, users = create_dummy_listings_for_testing(Main, 1)
        self.assertEquals(len(listings), 1)
        self.assertEquals(len(users), 1)
        owner = users[0]
        listing = listings[0]
        self.owner_id = owner['userId']
        self.owner_token = owner['authToken']
        self.listing_id = listing['listingId']

        # now create a new user as a liker
        users = create_dummy_users_for_testing(Main, 1)
        self.assertEquals(len(users), 1)
        liker = users[0]
        self.liker_id = liker['userId']
        self.liker_token = liker['authToken']

    def test_owner_liking_listing(self):
        like_the_listing = {
            "userId": self.owner_id,
            "listingId": self.listing_id,
            'authToken': self.owner_token,
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)

        errors_expected = [unallowed_liked['error']]
        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_like_listing(self):
        like_the_listing = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)

    def test_already_liked_listing(self):

        like_the_listing = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "True"
        }
        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)

        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)
        errors_expected = [duplicated_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_dislike_listing(self):
        dislike_the_listing = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "False"
        }

        request = webapp2.Request.blank('/like', POST=dislike_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)

    def test_disliking_like(self):

        dislike_the_listing_again = {
            "userId": self.liker_id,
            "listingId": self.listing_id,
            "authToken": self.liker_token,
            "liked": "False"
        }

        request = webapp2.Request.blank('/like', POST=dislike_the_listing_again)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)

        request = webapp2.Request.blank('/like', POST=dislike_the_listing_again)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)
        errors_expected = [duplicated_liked['error']]
        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_missing_user_input(self):
        like_with_missing_input = {
            "userId": "",
            "listingId": "",
            "authToken": "",
            "liked": ""
        }

        request = webapp2.Request.blank('/like', POST=like_with_missing_input)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [missing_user_id['error'],
                           missing_listing_id['error'],
                           missing_liked['error'],
                           missing_token['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_invalid_user_input(self):
        like_with_invalid_input = {
            "userId": "supposed to be an integer",
            "listingId": "supposed to be an integer",
            "authToken": self.liker_token,
            "liked": "supposed to be a boolean"
        }

        request = webapp2.Request.blank('/like',
                                        POST=like_with_invalid_input)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [invalid_user_id['error'],
                           invalid_listing_id['error'],
                           invalid_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
