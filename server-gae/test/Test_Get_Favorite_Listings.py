from __future__ import absolute_import

import os
import unittest

import Main
import extras.Error_Code as Error_Code
from web_apis.Create_User import *
from extras.utils import get_response_from_post
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlers(unittest.TestCase):
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

        # make the liker likes the first five of the listings

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[0]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[1]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[2]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[3]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, listings[4]['listingId'], "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        # the first five listings has been liked, so we create a list of those listings for future use
        self.likedListings = listings[0:5]

    def test_get_fav_listings(self):

        #######################################################################3
        # test case 1: successful get info

        getFavs = {
            "userId": self.likerId
        }

        request = webapp2.Request.blank('/getFavourites', POST=getFavs)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        output = json.loads(response.body)

        # get the number of published listings
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

        request = webapp2.Request.blank('/getFavourites', POST=invalidFavs)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

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


def get_like_post_dictionary(userId, listingId, liked):
    return {"userId": userId, "listingId":
        listingId, "liked": liked}


def get_like_response(POST):
    return get_response_from_post(Main, POST, 'like')

def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
