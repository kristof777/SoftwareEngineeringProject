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
        empty_input = {}
        request = webapp2.Request.blank('/createListing',
                                        POST=empty_input)
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
                           missing_published['error'],
                           missing_token['error'],
                           missing_longitude['error'],
                           missing_latitude['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_empty_fields(self):
        input = {"userId": "",
                 "authToken": "",
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
                 "longitude": "",
                 "latitude": "",
                 "images": ''
                 }

        request = webapp2.Request.blank('/createListing', POST=input)
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
                           missing_published['error'],
                           missing_token['error'],
                           missing_longitude['error'],
                           missing_latitude['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_multiple_spaces_input(self):
        input = {"userId": "      ",
                 "authToken": "      ",
                 "bedrooms": "       ",
                 "squarefeet": "        ",
                 "bathrooms": "      ",
                 "price": "        ",
                 "description": "      ",
                 "isPublished": "      ",
                 "province": "       ",
                 "city": "       ",
                 "address": "      ",
                 "longitude": "   ",
                 "latitude": "   ",
                 "thumbnailImageIndex": "      ",
                 "images": '    '
                 }

        request = webapp2.Request.blank('/createListing',
                                        POST=input)
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
                           missing_published['error'],
                           missing_token['error'],
                           missing_longitude['error'],
                           missing_latitude['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_some_missing_fields(self):
        missing_input = create_random_listing("", "")
        missing_input['squarefeet'] = ""
        missing_input['description'] = ""
        missing_input['city'] = ""
        missing_input['images'] = ''

        request = webapp2.Request.blank('/createListing',
                                        POST=missing_input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [missing_user_id['error'],
                           missing_token['error'],
                           missing_squarefeet['error'],
                           missing_description['error'],
                           missing_city['error'],
                           missing_image['error']]

        error_keys = [str(x) for x in json.loads(response.body)]
        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_invalid_user_id(self):
        input = create_random_listing("1111", "sfasdtr54523df")

        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, unauthorized_access)

        errors_expected = [not_authorized['error']]
        error_keys = [str(x) for x in json.loads(response.body)]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_invalid_numeric_field(self):
        input = create_random_listing("supposed to be int", "random token")
        input['bedrooms'] = "supposed to be int"
        input['squarefeet'] = "supposed to be int"
        input['bathrooms'] = "supposed to be float"
        input['price'] = "supposed to be int"
        input['thumbnailImageIndex'] = 'supposed to be int'
        input['longitude'] = 'supposed to be float'
        input['latitude'] = 'supposed to be float'

        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, missing_invalid_parameter)

        errors_expected = [invalid_user_id['error'],
                           invalid_bedrooms['error'],
                           invalid_squarefeet['error'],
                           invalid_bathrooms['error'],
                           invalid_price['error'],
                           invalid_longitude['error'],
                           invalid_latitude['error'],
                           invalid_thumbnail_image_index['error']
                           ]

        error_keys = [str(x) for x in json.loads(response.body)]

        self.assertTrue(are_two_lists_same(error_keys, errors_expected))

    def test_correct_input(self):
        inputs, users = create_dummy_listings_for_testing(Main, 1)
        correct_input = inputs[0]
        request = webapp2.Request.blank('/createListing', POST=correct_input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, success)

        output = json.loads(response.body)
        self.assertTrue("listingId" in output)

        listing_created = Listing.get_by_id(int(output["listingId"]))
        self.assertEquals(listing_created.bedrooms, int(correct_input['bedrooms']))
        self.assertEquals(listing_created.squarefeet, int(correct_input['squarefeet']))
        self.assertEquals(listing_created.bathrooms, float(correct_input['bathrooms']))
        self.assertEquals(listing_created.price, int(correct_input['price']))
        self.assertEquals(listing_created.description, correct_input['description'])
        self.assertEquals(str(listing_created.isPublished), correct_input['isPublished'])
        self.assertEquals(listing_created.province, correct_input['province'])
        self.assertEquals(listing_created.city, correct_input['city'])
        self.assertEquals(listing_created.address, correct_input['address'])
        self.assertEquals(listing_created.thumbnailImageIndex, int(correct_input['thumbnailImageIndex']))
        self.assertEquals(listing_created.images, json.loads(correct_input['images']))

    def tearDown(self):
        self.testbed.deactivate()


def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
