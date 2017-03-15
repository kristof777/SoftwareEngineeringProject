from __future__ import absolute_import

import os
import sys
import unittest
from extras.utils import *
import Main
import extras.Error_Code as Error_Code
from models import Favorite
from models.Listing import Listing
from web_apis.Create_User import *

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlers(unittest.TestCase):
    """
        test case 1: missing input
        test case 2: unauthorized identifier
        test case 3: success delivery

    """
    def setUp(self):
        setup_testbed(self)

        # create a user as well as a listing that the user owns
        listings, users = create_dummy_listings_for_testing(Main, 1)
        assert len(listings) == 1
        assert len(users) == 1
        owner = users[0]
        listing = listings[0]
        self.ownerId = owner['userId']
        self.ownerToken = owner['authToken']
        self.listingId = listing['listingId']

        # now create a new user as an editor
        users = create_dummy_users_for_testing(Main, 2)
        assert len(users) == 2
        deleter = users[0]
        self.deleterId = deleter['userId']
        self.deleterToken = deleter['authToken']
        liker = users[1]
        self.likerId = liker['userId']
        self.likerToken = liker['authToken']

        # Make the liker like the listing
        res_value, status = get_like_response(get_like_post_dictionary(self.likerId, self.listingId,
                                                                       self.likerToken, "True"))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

    def test_missing_input(self):
        res_value, status = get_delete_response(get_delete_post_dictionary("", "", ""))

        self.assertEqual(status, missing_invalid_parameter)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_listing_id['error'],
                           Error_Code.missing_token['error']]
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_listing_auth(self):

        res_value, status = get_delete_response(
            get_delete_post_dictionary(self.deleterId, self.listingId, self.deleterToken))
        self.assertEquals(status, not_authorized['status'])
        error_expected = Error_Code.not_authorized['error']
        self.assertTrue(error_expected in res_value)

    def invalid_user_id(self):
        res_value, status = get_delete_response(get_delete_post_dictionary("blabla", "blabla", self.ownerToken))
        self.assertEquals(status, missing_invalid_parameter)
        errors_expected = [Error_Code.invalid_user_id['error'],
                           Error_Code.invalid_listing_id['error']]
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_correct_input(self):
        res_value, status = get_delete_response(
            get_delete_post_dictionary(self.ownerId, self.listingId, self.ownerToken))
        self.assertEquals(status, success)

        listing_changed = Listing.get_by_id(self.listingId)
        self.assertEquals(listing_changed, None)

    def tearDown(self):
        self.testbed.deactivate()


def get_like_post_dictionary(userId, listingId, token, liked):
    return {"userId": userId, "listingId":
        listingId, "authToken": token, "liked": liked}


def get_like_response(POST):
    return get_response_from_post(Main, POST, 'like')


def get_delete_post_dictionary(userId, listingId, token):
    return {"userId": userId, "listingId":
        listingId, "authToken": token}


def get_delete_response(POST):
    request = webapp2.Request.blank('/deleteListing', POST=POST)
    response = request.get_response(Main.app)
    return json.loads(response.body), response.status_int



def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
