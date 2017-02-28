import unittest
import Main
from google.appengine.ext import testbed
from web_apis.Like_Dislike_Listing import *
from __future__ import absolute_import
import sys
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


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

    def test_like_dislike_a_listing(self):

        # create a user as well as a listing that the user owns
        listings, users = create_dummy_listings_for_testing(Main, 1)
        assert len(listings) == 1
        assert len(users) == 1
        owner = users[0]
        listing = listings[0]
        ownerId = owner['userId']
        listingId = listing['listingId']

        # now create a new user as a liker
        users = create_dummy_users_for_testing(1, Main)
        assert len(users) == 1
        liker = users[0]
        likerId = liker['userId']

        #########################################################################################################
        # test case 1: the owner can't like their listings

        # now user want to like the listing
        likeTheListing = {
            "userId": ownerId,
            "listingId": listingId,
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)

        errors_expected = [unallowed_liked['error']]

        # checking if there is a difference between error_keys and what we got
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(unallowed_liked['error'], errors_expected)

        #####################################################################################################
        # test case 2: successful delivery (like the listing)

        likeTheListing = {
            "userId": likerId,
            "listingId": listingId,
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)


        ########################################################################################################
        # test case 3: send a like request(liked==True) while the listing is already liked
        likeTheListing = {
            "userId": likerId,
            "listingId": listingId,
            "liked": "True"
        }

        # likeTheListing["userId"] = likerId
        # likeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
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

        dislikeTheListing = {
            "userId": likerId,
            "listingId": listingId,
            "liked": "False"
        }

        request = webapp2.Request.blank('/like', POST=dislikeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        ########################################################################################################
        # test case 5: dislike this listing again
        dislikeTheListingAgain = {
            "userId": likerId,
            "listingId": listingId,
            "liked": "False"
        }

        request = webapp2.Request.blank('/like', POST=dislikeTheListingAgain)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.duplicated_liked['error']]

        # checking if there is a difference between error_keys and what we got
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(duplicated_liked['error'], errors_expected)

        ########################################################################################################
        # test case 6: missing user input

        likeWithMissingInput = {
            "userId": "",
            "listingId": "",
            "liked": ""
        }

        request = webapp2.Request.blank('/like', POST=likeWithMissingInput)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        errors_expected = [missing_user_id['error'],
                           missing_listing_id['error'],
                           missing_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

        ########################################################################################################
        # test case 7: invalid user input

        likeWithInvalidInput = {
            "userId": "supposed to be an integer",
            "listingId": "supposed to be an integer",
            "liked": "supposed to be a boolean"
        }

        request = webapp2.Request.blank('/like', POST=likeWithInvalidInput)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
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
