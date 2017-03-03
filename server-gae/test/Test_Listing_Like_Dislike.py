from __future__ import absolute_import

import sys
import unittest

import Main
from web_apis.Like_Dislike_Listing import *

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlers(unittest.TestCase):
    def setUp(self):
        setup_testbed(self)

        # create a user as well as a listing that the user owns
        listings, users = create_dummy_listings_for_testing(Main, 1)
        assert len(listings) == 1
        assert len(users) == 1
        owner = users[0]
        listing = listings[0]
        self.ownerId = owner['userId']
        self.listingId = listing['listingId']

        # now create a new user as a liker
        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        liker = users[0]
        self.likerId = liker['userId']

    def test_like_dislike_a_listing(self):

        #########################################################################################################
        # test case 1: the owner can't like their listings

        # now user want to like the listing
        like_the_listing = {
            "userId": self.ownerId,
            "listingId": self.listingId,
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)

        errors_expected = [unallowed_liked['error']]

        # checking if there is a difference between error_keys and what we got
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(unallowed_liked['error'], errors_expected)

        #####################################################################################################
        # test case 2: successful delivery (like the listing)

        like_the_listing = {
            "userId": self.likerId,
            "listingId": self.listingId,
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)


        ########################################################################################################
        # test case 3: send a like request(liked==True) while the listing is already liked
        like_the_listing = {
            "userId": self.likerId,
            "listingId": self.listingId,
            "liked": "True"
        }

        # likeTheListing["userId"] = likerId
        # likeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=like_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)
        errors_expected = [duplicated_liked['error']]

        # checking if there is a difference between error_keys and what we got
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(duplicated_liked['error'], errors_expected)

        ########################################################################################################
        # test case 4: dislike this listing
        # should be a successful delivery

        dislike_the_listing = {
            "userId": self.likerId,
            "listingId": self.listingId,
            "liked": "False"
        }

        request = webapp2.Request.blank('/like', POST=dislike_the_listing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)

        ########################################################################################################
        # test case 5: dislike this listing again
        dislike_the_listing_again = {
            "userId": self.likerId,
            "listingId": self.listingId,
            "liked": "False"
        }

        request = webapp2.Request.blank('/like', POST=dislike_the_listing_again)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, processing_failed)
        errors_expected = [duplicated_liked['error']]

        # checking if there is a difference between error_keys and what we got
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(duplicated_liked['error'], errors_expected)

        ########################################################################################################
        # test case 6: missing user input

        like_with_missing_input = {
            "userId": "",
            "listingId": "",
            "liked": ""
        }

        request = webapp2.Request.blank('/like', POST=like_with_missing_input)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [missing_user_id['error'],
                           missing_listing_id['error'],
                           missing_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

        ########################################################################################################
        # test case 7: invalid user input

        like_with_invalid_input = {
            "userId": "supposed to be an integer",
            "listingId": "supposed to be an integer",
            "liked": "supposed to be a boolean"
        }

        request = webapp2.Request.blank('/like', POST=like_with_invalid_input)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, missing_invalid_parameter)
        errors_expected = [invalid_user_id['error'],
                           invalid_listing_id['error'],
                           invalid_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
