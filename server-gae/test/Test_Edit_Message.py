from __future__ import absolute_import

import os
import sys

sys.path.append("../")
import unittest
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Main
from web_apis.Create_User import *
import extras.utils as utils
from models.Message import Message


class TestEditMessage(unittest.TestCase):
    """
    Test case 1: Correct delete input
    Test case 2: Correct read input
    Test case 3: missing userId, token, messageId
    Test case 4: invalid userId, token, messageId
    Test case 5: messageId is integer but user still doesn't exist
    Test case 6: already liked listing

    """
    def setUp(self):
        setup_testbed(self)
        self.user_buyer = create_dummy_users_for_testing(Main, 1)[0]
        listings, user_sellers = create_dummy_listings_for_testing(Main,1)
        self.user_seller = user_sellers[0]
        self.listing = listings[0]

        message_input = {
            "senderId": self.user_buyer['userId'],
            "listingId": self.listing['listingId'],
            "authToken": self.user_buyer['token'],
            "message": "Hey, I'm interested in your property.",
            "phone": self.user_buyer['phone1'],
            "email": self.user_buyer['email']
        }
        utils.get_response_from_post(Main, message_input, 'contactSeller')
        #TODO assert response here
        # Will need get my listing here to make this testing work
        self.message_id_1 = 4
        self.message_id_2 = 2


    def test_correct_input_read(self):
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["token"],
                                          self.message_id_1, 'r')
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        self.assertEquals(response_status, success)
        message = Message.get_by_id(self.message_id_1)
        self.assertTrue(message.received)

    def test_correct_input_delete(self):
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["token"],
                                          self.message_id_1, 'd')
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        self.assertEquals(response_status, success)
        message = Message.get_by_id(self.message_id_1)
        self.assertIsNone(message)

    def test_missing_fields(self):
        testing_input = {}
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        error_keys = ['messageId', 'userId', 'authToken', 'readDel']
        expected_errors = [missing[key]["error"] for key in error_keys]
        self.assertEquals(response_status, missing_invalid_parameter)
        error_keys_received = get_keys_from_values(values)
        self.assertSetEqual(set(expected_errors), set(error_keys_received))

    def test_invalid_field(self):
        testing_input = get_testing_input("as", "asdfjhasdkfh", "asd", "112")
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')

        error_keys = ['messageId', 'userId', 'readDel']
        expected_errors = [invalids[key]["error"] for key in error_keys]
        self.assertEquals(response_status, missing_invalid_parameter)
        error_keys_received = get_keys_from_values(values)
        self.assertSetEqual(set(expected_errors), set(error_keys_received))

    def test_incorrect_message_id(self):
        testing_input = get_testing_input(self.user_seller["userId"],
                                          self.user_seller["token"],
                                          self.message_id_2, 'd')
        values, response_status = \
            utils.get_response_from_post(Main, testing_input, 'editMessage')
        expected_errors = [invalid_message_id["error"]]
        self.assertEquals(response_status, missing_invalid_parameter)
        error_keys_received = get_keys_from_values(values)
        self.assertSetEqual(set(expected_errors), set(error_keys_received))

    def test_liked_listing(self):
        self.test_correct_input_read()
        self.test_correct_input_read()





    def tearDown(self):
        self.testbed.deactivate()



def get_testing_input(user_id, user_auth_token,message_id, read_del):
    return {
        "userId": user_id,
        "authToken": user_auth_token,
        "messageId": message_id,
        "readDel": read_del
    }

def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
