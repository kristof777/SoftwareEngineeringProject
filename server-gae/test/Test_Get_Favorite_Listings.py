from __future__ import absolute_import
import unittest
import json
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import extras.Error_Code as Error_Code
import Main
from google.appengine.ext import testbed
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

        # create 10 listings for a user
        listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(listings) == 10

        # now create a new user as a liker
        users = create_dummy_users_for_testing(1, Main)
        assert len(users) == 1
        liker = users[0]
        self.likerId = liker['userId']

        # make the liker likes the first five of the listings
        likeTheListing = {
            "userId": self.likerId,
            "listingId": listings[0]['listingId'],
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        likeTheListing = {
            "userId": self.likerId,
            "listingId": listings[1]['listingId'],
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        likeTheListing = {
            "userId": self.likerId,
            "listingId": listings[2]['listingId'],
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        likeTheListing = {
            "userId": self.likerId,
            "listingId": listings[3]['listingId'],
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        likeTheListing = {
            "userId": self.likerId,
            "listingId": listings[4]['listingId'],
            "liked": "True"
        }

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        # the first five listings has been liked
        self.likedListings = listings[0:5]


    def test_get_fav_listings(self):

        #######################################################################3
        # test case 1: successful get info

        getFavs = {
            "userId": self.likerId
        }

        request = webapp2.Request.blank('/getFavoriteListing', POST=getFavs)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        isPublishes = 0
        for listing in self.likedListings:
            if listing['isPublished'] == 'True':
                isPublishes += 1

        self.assertEquals(len(output["listings"]), isPublishes)

        #######################################################################3
        # test case 2: invalid userId

        invalidFavs = {
            "userId": "blablabla"
        }

        request = webapp2.Request.blank('/getFavoriteListing', POST=invalidFavs)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.invalid_user_id['error']]

        # checking if there is a difference between error_keys and what we got
        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(invalid_user_id['error'], errors_expected)



    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()

def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
