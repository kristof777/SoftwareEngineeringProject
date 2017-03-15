from __future__ import absolute_import

import os
import unittest

import Main
import extras.Error_Code as Error_Code
from web_apis.Create_User import *
from extras.utils import get_response_from_post
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestGetMessages(unittest.TestCase):
    """
    Test cases
    successful get info
    Invalid userId
    """
    def setUp(self):
        setup_testbed(self)

        # create 10 listings for one user
        listings, users = create_dummy_listings_for_testing(Main, 10)
        assert len(users) == 1
        assert len(listings) == 10
        self.seller = users[0]
        self.listings = listings

        self.messagers = create_dummy_users_for_testing(Main, 3)
        assert len(self.messagers) == 3

        res_value, status = get_contact_response(get_contact_seller_post_dictionary(self.messagers[0]['userId'],
                                                                                 self.seller['userId'],
                                                                                 self.listings[0]['listingId'],
                                                                                 self.messagers[0]['authToken'],
                                                                                 "Interested in your listing!",
                                                                                 self.messagers[0]['phone1'],
                                                                                 self.messagers[0]['email']))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_contact_response(get_contact_seller_post_dictionary(self.messagers[1]['userId'],
                                                                                 self.seller['userId'],
                                                                                 self.listings[1]['listingId'],
                                                                                 self.messagers[1]['authToken'],
                                                                                 "Any time we can meet up?",
                                                                                 self.messagers[1]['phone1'],
                                                                                 self.messagers[1]['email']))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

        res_value, status = get_contact_response(get_contact_seller_post_dictionary(self.messagers[2]['userId'],
                                                                                 self.seller['userId'],
                                                                                 self.listings[2]['listingId'],
                                                                                 self.messagers[2]['authToken'],
                                                                                 "Nice house!",
                                                                                 self.messagers[2]['phone1'],
                                                                                 self.messagers[2]['email']))
        self.assertEqual(status, success)
        self.assertEquals(res_value, None)

    def test_success(self):
        get_messages = {
            "userId": self.seller['userId'],
            "authToken": self.seller['authToken']
        }
        request = webapp2.Request.blank('/getMessages', POST=get_messages)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, success)
        output = json.loads(response.body)
        self.assertEquals(len(output['messages']), 3)

    def test_invalid_userid(self):
        invalid_userId_messages = {
            "userId": "blablabla",
            "authToken": self.seller['authToken']
        }

        request = webapp2.Request.blank('/getMessages', POST=invalid_userId_messages)
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


def get_contact_seller_post_dictionary(sender_id, receiver_id, listing_id, auth_token, message,phone, email):
    return {
            "senderId": sender_id,
            "receiverId": receiver_id,
            "listingId": listing_id,
            "authToken": auth_token,
            "message": message,
            "phone": phone,
            "email": email
        }


def get_contact_response(POST):
    return get_response_from_post(Main, POST, 'contactSeller')


def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
