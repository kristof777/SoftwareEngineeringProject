from __future__ import absolute_import

import os
import sys

sys.path.append("../")
import unittest
from API_NAME import contact_seller_api

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *


class TestHandlers(unittest.TestCase):
    def setUp(self):
        setup_testbed(self)
        self.user_buyer = create_dummy_users_for_testing(Main, 1)[0]
        listings, user_sellers = create_dummy_listings_for_testing(Main, 1)
        self.user_seller = user_sellers[0]
        self.listing = listings[0]

    def test_correct_input(self):
        correct_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": self.listing['listingId'],
            "authToken": self.user_buyer['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email'],
            "receiverId": self.user_seller['userId']
        }

        response, response_status = get_response_from_post(Main,
                                                           correct_input,
                                                           contact_seller_api)
        self.assertEquals(response_status, success)

    def test_unallowed_input(self):
        unallowed_input = {
            "senderId": self.user_seller['userId'],
            "listingId": self.listing['listingId'],
            "receiverId": self.user_seller['userId'],
            "authToken": self.user_seller['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }

        response, response_status = get_response_from_post(Main,
                                                           unallowed_input,
                                                           contact_seller_api)
        self.assertEquals(response_status, processing_failed)
        errors_expected = [unallowed_message_send['error']]
        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_unauthorized_user_id_input(self):
        unauthorized_input = {
            "senderId": 111,
            "listingId": self.listing['listingId'],
            "authToken": self.user_buyer['authToken'],
            "receiverId": self.user_seller['userId'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }

        response, response_status = get_response_from_post(Main,
                                                           unauthorized_input,
                                                           contact_seller_api)

        self.assertEquals(response_status, not_authorized['status'])
        errors_expected = [not_authorized['error']]
        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_unauthorized_listingId_input(self):
        unauthorized_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": 111,
            "receiverId": self.user_seller['userId'],
            "authToken": self.user_buyer['authToken'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }

        response, response_status = get_response_from_post(Main,
                                                           unauthorized_input,
                                                           contact_seller_api)
        self.assertEquals(response_status, un_auth_listing['status'])
        errors_expected = [un_auth_listing['error']]
        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_missing_input(self):
        missing_input = {}
        response, response_status = get_response_from_post(Main,
                                                           missing_input,
                                                           contact_seller_api)

        self.assertEquals(response_status, missing_invalid_parameter)

        errors_expected = [missing_senderId['error'],
                           missing_listing_id['error'],
                           missing_message['error'],
                           missing_phone_number['error'],
                           missing_email['error'],
                           missing_token['error'],
                           missing_receiverId['error']]
        error_keys = [str(x) for x in response]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def tearDown(self):
        self.testbed.deactivate()
