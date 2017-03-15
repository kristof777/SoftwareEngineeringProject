from __future__ import absolute_import

import os
import sys
import unittest

import Main
import extras.Error_Code as Error_Code
from models.Listing import Listing
from web_apis.Create_User import *

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlers(unittest.TestCase):
    """
        test case 1: missing input
        test case 2: missing key-value pair
        test case 3: unrecognized key
        test case 4: the editor, which is not the owner, cannot edit the listing
        test case 5: invalid userId and listingId
        test case 6: unauthorized userId and listingId
        test case 7: input with invalid fields
        test case 8: correct input

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
        self.token = owner['authToken']
        self.listingId = listing['listingId']

        # now create a new user as an editor
        users = create_dummy_users_for_testing(Main, 1)
        assert len(users) == 1
        editors = users[0]
        self.editorId = editors['userId']
        self.editorToken = editors['authToken']


    def test_missing_input(self):
        res_value, status = get_response(get_post_dictionary("", "", "", {}))

        self.assertEqual(status, missing_invalid_parameter)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_listing_id['error'],
                           Error_Code.missing_token['error']]
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_missing_key_value(self):
        change_values = {
                "province": "",
                "city": "   ",
                "bathrooms": "",
                "description": "  ",
        }

        res_value, status = get_response(get_post_dictionary(self.ownerId, self.listingId, self.token, change_values))

        self.assertEqual(status, missing_invalid_parameter)

        errors_expected = [Error_Code.missing_province['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_bathrooms['error'],
                           Error_Code.missing_description['error']]

        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_unrecognized_key(self):
        change_values = { "blablabla": "blablabla"}
        res_value, status = get_response(get_post_dictionary(self.ownerId, self.listingId, self.token, change_values))
        self.assertEqual(status, unrecognized_key["status"])
        error_expected = Error_Code.unrecognized_key['error']
        self.assertTrue(error_expected in res_value)

    def test_listing_auth(self):
        change_values = {"bathrooms": 10}

        res_value, status = get_response(
            get_post_dictionary(self.editorId, self.listingId, self.editorToken, change_values))
        self.assertEquals(status, not_authorized['status'])
        error_expected = Error_Code.not_authorized['error']
        self.assertTrue(error_expected in res_value)

    def invalid_user_id(self):
        change_values = {"bathrooms": 10}
        res_value, status = get_response(get_post_dictionary("blabla", "blabla", self.token, change_values))
        self.assertEquals(status, missing_invalid_parameter)
        errors_expected = [Error_Code.invalid_user_id['error'],
                           Error_Code.invalid_listing_id['error']]
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_unauthorized_userid_listing_id(self):
        change_values = {"bathrooms": 10}
        res_value, status = get_response(get_post_dictionary(1111111, 4444444, self.token, change_values))
        self.assertEquals(status, not_authorized['status'])
        error_expected = Error_Code.not_authorized['error']
        self.assertTrue(error_expected in res_value)

    def test_invalid_fields(self):
        change_values = { "bedrooms": "supposed to be a number",
                            "squarefeet": "supposed to be a number",
                            "bathrooms": "supposed to be a number",
                            "price": "supposed to be a number",
                            "isPublished": "supposed to be a boolean",
                            "city": "Regina",
                            "address": "312 Summer Place",
                            "thumbnailImageIndex": "supposed to be a number"
                          }

        res_value, status = get_response(get_post_dictionary(self.ownerId, self.listingId, self.token, change_values))

        self.assertEquals(status, missing_invalid_parameter)

        errors_expected = [Error_Code.invalid_bedrooms['error'],
                           Error_Code.invalid_squarefeet['error'],
                           Error_Code.invalid_bathrooms['error'],
                           Error_Code.invalid_price['error'],
                           Error_Code.invalid_thumbnail_image_index['error'],
                           Error_Code.invalid_published['error']]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(res_value, errors_expected), True)

    def test_correct_input(self):
        change_values = {"bedrooms": "4",
                         "squarefeet": "1500",
                         "bathrooms": "5",
                         "price": "2050000",
                         "isPublished": "False",
                         "city": "Regina",
                         "address": "312 Summer Place",
                         "thumbnailImageIndex": 1
                         }

        res_value, status = get_response(
            get_post_dictionary(self.ownerId, self.listingId, self.token, change_values))
        self.assertEquals(status, success)
        listing_changed = Listing.get_by_id(self.listingId)
        self.assertEquals(listing_changed.bedrooms,
                          int(change_values['bedrooms']))
        self.assertEquals(listing_changed.squarefeet, int(change_values['squarefeet']))
        self.assertEquals(listing_changed.bathrooms,
                          float(change_values['bathrooms']))
        self.assertEquals(listing_changed.price, int(change_values['price']))
        self.assertEquals(str(listing_changed.isPublished),
                          change_values['isPublished'])
        self.assertEquals(listing_changed.city, change_values['city'])
        self.assertEquals(listing_changed.address, change_values['address'])
        self.assertEquals(listing_changed.thumbnailImageIndex,
                          int(change_values['thumbnailImageIndex']))

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def get_post_dictionary(userId, listingId, token, change_values):
    return {"userId": userId, "listingId":
        listingId, "authToken": token, "changeValues": json.dumps(change_values)}


def get_response(POST):
    request = webapp2.Request.blank('/editListing', POST=POST)
    response = request.get_response(Main.app)
    return json.loads(response.body), response.status_int


def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
