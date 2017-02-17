import unittest
import webapp2
import os
import main
import json
import error_code
from models.user import User
from models.listing import Listing
from google.appengine.ext import db
from google.appengine.ext import testbed
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

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

        # test case 1
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

        request = webapp2.Request.blank('/createlisting', POST=input)  # api you need to test
        response = request.get_response(main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [error_code.missing_user_id['error'],
                           error_code.missing_bedrooms['error'],
                           error_code.missing_sqft['error'],
                           error_code.missing_bathrooms['error'],
                           error_code.missing_price['error'],
                           error_code.missing_description['error'],
                           error_code.missing_province['error'],
                           error_code.missing_city['error'],
                           error_code.missing_address['error'],
                           error_code.missing_image['error'],
                           error_code.missing_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ###########################################################################
        # test case 2: there're some missing fields
        input = {"userId": "",
                 "bedrooms": "2",
                 "sqft": "",
                 "bathrooms": "2",
                 "price": "200000",
                 "description": "",
                 "isPublished": "True",
                 "province": "Saskatchewan",
                 "city": "",
                 "address": "91 Campus Dr.",
                 "thumbnailImageIndex": 0,
                 "images": ''
                 }

        request = webapp2.Request.blank('/createlisting', POST=input)  # api you need to test
        response = request.get_response(main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [error_code.missing_user_id['error'],
                           error_code.missing_sqft['error'],
                           error_code.missing_description['error'],
                           error_code.missing_city['error'],
                           error_code.missing_image['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ###########################################################################
        # test case 3
        # checking if all error codes are received, if there's a non-existing userId
        input = {"userId": "1",
                  "bedrooms": "2",
                  "sqft": "1200",
                  "bathrooms": "2",
                  "price": "200000",
                  "description": "This is a nice house",
                  "isPublished": "True",
                  "province": "Saskatchewan",
                  "city": "Saskatoon",
                  "address": "91 Campus Dr.",
                  "thumbnailImageIndex": 0,
                  "images": 'some images'
                  }

        request = webapp2.Request.blank('/createlisting', POST=input)
        response = request.get_response(main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [error_code.un_auth_listing['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        ###########################################################################
        # test case 4
        # checking if all error codes are received, if all numeric fields are invalid
        input = {"userId": "supposed to be int",
                 "bedrooms": "supposed to be int",
                 "sqft": "supposed to be int",
                 "bathrooms": "supposed to be int",
                 "price": "supposed to be int",
                 "description": "This is a nice house",
                 "isPublished": "True",
                 "province": "Saskatchewan",
                 "city": "Saskatoon",
                 "address": "91 Campus Dr.",
                 "thumbnailImageIndex": "supposed to be int",
                 "images": 'some images'
                 }

        request = webapp2.Request.blank('/createlisting', POST=input)
        response = request.get_response(main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [error_code.invalid_user_id['error'],
                           error_code.un_auth_listing['error'],
                           error_code.invalid_bedrooms['error'],
                           error_code.invalid_sqft['error'],
                           error_code.invalid_bathrooms['error'],
                           error_code.invalid_price['error'],
                           error_code.invalid_thumbnail_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #############################################################################
        # test case 5: correct input
        # Note that the user along with the userId is created on melody's local host,
        # so it shouldn't be working on other computer
        input = {"userId": "5681726336532480",
                  "bedrooms": "2",
                  "sqft": "1200",
                  "bathroom": "2",
                  "price": "200000",
                  "description": "This is a nice house",
                  "isPublished": "True",
                  "province": "Saskatchewan",
                  "city": "Saskatoon",
                  "address": "91 Campus Dr.",
                  "thumbnailImageIndex": 0,
                  "images": 'some images'
                  }
        #FIXME
        # request = webapp2.Request.blank('/createlisting', POST=input)
        # response = request.get_response(main.app)
        #
        # self.assertEquals(response.status_int, 200)
        #
        # output = json.loads(response.body)
        # self.assertTrue("listingId" in output)








    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




if __name__ == '__main__':
    unittest.main()
