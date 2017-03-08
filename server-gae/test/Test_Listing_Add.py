from __future__ import absolute_import

import os
import sys
import unittest

import Main
from models.Listing import Listing
from web_apis.Create_User import *

sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class TestHandlers(unittest.TestCase):
    """
        test case 1: empty object as input
        test case 2
        checking if all error codes are received, if empty code is sent
        test case 3
        checking if all error codes are received, if all user inputs are spaces
        test case 4: there're some missing fields
        test case 5# test case 6
        test case 7: correct input
    """
    def setUp(self):
        setup_testbed(self)

    def test_empty_input(self):
        input = {}
        request = webapp2.Request.blank('/createListing',
                                        POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_bedrooms['error'],
                           missing_squarefeet['error'],
                           missing_bathrooms['error'],
                           missing_price['error'],
                           missing_description['error'],
                           missing_province['error'],
                           missing_city['error'],
                           missing_address['error'],
                           missing_image['error'],
                           missing_image_index['error'],
                           missing_published['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

    def test_empty_fields(self):
        input = {"userId": "",
                 "bedrooms": "",
                 "squarefeet": "",
                 "bathrooms": "",
                 "price": "",
                 "description": "",
                 "isPublished": "",
                 "province": "",
                 "city": "",
                 "address": "",
                 "thumbnailImageIndex": "",
                 "images": ''
                 }

        request = webapp2.Request.blank('/createListing', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_bedrooms['error'],
                           missing_squarefeet['error'],
                           missing_bathrooms['error'],
                           missing_price['error'],
                           missing_description['error'],
                           missing_province['error'],
                           missing_city['error'],
                           missing_address['error'],
                           missing_image['error'],
                           missing_image_index['error'],
                           missing_published['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

    def test_multiple_spaces_input(self):
        input = {"userId": "      ",
                 "bedrooms": "       ",
                 "squarefeet": "        ",
                 "bathrooms": "      ",
                 "price": "        ",
                 "description": "      ",
                 "isPublished": "      ",
                 "province": "       ",
                 "city": "       ",
                 "address": "      ",
                 "thumbnailImageIndex": "      ",
                 "images": '    '
                 }

        request = webapp2.Request.blank('/createListing',
                                        POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_bedrooms['error'],
                           missing_squarefeet['error'],
                           missing_bathrooms['error'],
                           missing_price['error'],
                           missing_description['error'],
                           missing_province['error'],
                           missing_city['error'],
                           missing_address['error'],
                           missing_image['error'],
                           missing_image_index['error'],
                           missing_published['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

    def test_some_missing_fields(self):
        input = create_random_listing("")
        input['squarefeet'] = ""
        input['description'] = ""
        input['city'] = ""
        input['images'] = ''

        request = webapp2.Request.blank('/createListing',
                                        POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_squarefeet['error'],
                           missing_description['error'],
                           missing_city['error'],
                           missing_image['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

    def test_invalid_user_id(self):
        input = create_random_listing("1111")

        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, unauthorized_access)

        errors_expected = [not_authorized['error']]

        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(not_authorized['error'], errors_expected)

    def test_invalid_numeric_field(self):
        input = create_random_listing("supposed to be int")
        input['bedrooms'] = "supposed to be int"
        input['squarefeet'] = "supposed to be int"
        input['bathrooms'] = "supposed to be float"
        input['price'] = "supposed to be int"
        input['thumbnailImageIndex'] = 'supposed to be int'

        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [invalid_user_id['error'],
                           invalid_bedrooms['error'],
                           invalid_squarefeet['error'],
                           invalid_bathrooms['error'],
                           invalid_price['error'],
                           invalid_thumbnail_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

    def test_correct_input(self):
        inputs, users = create_dummy_listings_for_testing(Main, 1)
        input = inputs[0]
        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, success)

        output = json.loads(response.body)
        self.assertTrue("listingId" in output)

        listing_created = Listing.get_by_id(int(output["listingId"]))
        self.assertEquals(listing_created.bedrooms, int(input['bedrooms']))
        self.assertEquals(listing_created.squarefeet, int(input['squarefeet']))
        self.assertEquals(listing_created.bathrooms, float(input['bathrooms']))
        self.assertEquals(listing_created.price, int(input['price']))
        self.assertEquals(listing_created.description, input['description'])
        self.assertEquals(str(listing_created.isPublished), input['isPublished'])
        self.assertEquals(listing_created.province, input['province'])
        self.assertEquals(listing_created.city, input['city'])
        self.assertEquals(listing_created.address, input['address'])
        self.assertEquals(listing_created.thumbnailImageIndex, int(input['thumbnailImageIndex']))
        self.assertEquals(listing_created.images, input['images'])

    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
