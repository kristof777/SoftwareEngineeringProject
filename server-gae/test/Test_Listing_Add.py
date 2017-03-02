from __future__ import absolute_import
import json
import os
import unittest
import sys
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import extras.Error_Code as Error_Code
import Main
import webapp2
from google.appengine.ext import testbed
from models.Listing import Listing
from web_apis.Create_User import *


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

    def test_create_listings(self):
        # test case 1: empty object as input
        input = {}

        request = webapp2.Request.blank('/createListing', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [missing_user_id['error'],
                           missing_bedrooms['error'],
                           missing_sqft['error'],
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


        #################################################################
        # test case 2
        # checking if all error codes are received, if empty code is sent

        input = {"userId": "",
                 "bedrooms": "",
                 "sqft": "",
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

        self.assertEquals(response.status_int, 400)

        errors_expected = [missing_user_id['error'],
                           missing_bedrooms['error'],
                           missing_sqft['error'],
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

        #################################################################
        # test case 3
        # checking if all error codes are received, if all user inputs are spaces

        input = {"userId": "      ",
                 "bedrooms": "       ",
                 "sqft": "        ",
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

        request = webapp2.Request.blank('/createListing', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [missing_user_id['error'],
                           missing_bedrooms['error'],
                           missing_sqft['error'],
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

        ###########################################################################
        # test case 4: there're some missing fields

        input = create_random_listing("")
        input['sqft'] = ""
        input['description'] = ""
        input['city'] = ""
        input['images'] = ''

        request = webapp2.Request.blank('/createListing', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [missing_user_id['error'],
                           missing_sqft['error'],
                           missing_description['error'],
                           missing_city['error'],
                           missing_image['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)


        ###########################################################################
        # test case 5
        # checking if all error codes are received, if there's a non-existing userId

        input = create_random_listing("1111")

        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [un_auth_listing['error']]

        try:
            errors_expected = str(json.loads(response.body).keys()[0])
        except IndexError as _:
            self.assertFalse()

        self.assertEquals(un_auth_listing['error'], errors_expected)

        ###########################################################################
        # test case 6
        # checking if all error codes are received, if all numeric fields are invalid

        input = create_random_listing("supposed to be int")
        input['bedrooms'] = "supposed to be int"
        input['sqft'] = "supposed to be int"
        input['bathrooms'] = "supposed to be float"
        input['price'] = "supposed to be int"

        request = webapp2.Request.blank('/createListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [invalid_user_id['error'],
                           invalid_bedrooms['error'],
                           invalid_sqft['error'],
                           invalid_bathrooms['error'],
                           invalid_price['error'],
                           invalid_thumbnail_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(are_two_lists_same(error_keys, errors_expected), True)

        #############################################################################
        # test case 7: correct input

        inputs, users = create_dummy_listings_for_testing(Main, 1)
        input = inputs[0]
        request = webapp2.Request.blank('/creatListing', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 200)

        output = json.loads(response.body)
        self.assertTrue("listingId" in output)

        listing_created = Listing.get_by_id(int(output["listingId"]))
        self.assertEquals(listing_created.bedrooms, int(input['bedrooms']))
        self.assertEquals(listing_created.sqft, int(input['sqft']))
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
