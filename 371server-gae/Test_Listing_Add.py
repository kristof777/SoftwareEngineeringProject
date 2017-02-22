import unittest
import json
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import Error_Code
import Main
import webapp2
from google.appengine.ext import testbed
from models.Listing import Listing
from Create_User import *
import utils



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

        request = webapp2.Request.blank('/createlisting', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_bedrooms['error'],
                           Error_Code.missing_sqft['error'],
                           Error_Code.missing_bathrooms['error'],
                           Error_Code.missing_price['error'],
                           Error_Code.missing_description['error'],
                           Error_Code.missing_province['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_address['error'],
                           Error_Code.missing_image['error'],
                           Error_Code.missing_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)





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

        request = webapp2.Request.blank('/createlisting', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_bedrooms['error'],
                           Error_Code.missing_sqft['error'],
                           Error_Code.missing_bathrooms['error'],
                           Error_Code.missing_price['error'],
                           Error_Code.missing_description['error'],
                           Error_Code.missing_province['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_address['error'],
                           Error_Code.missing_image['error'],
                           Error_Code.missing_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

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

        request = webapp2.Request.blank('/createlisting', POST=input)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_bedrooms['error'],
                           Error_Code.missing_sqft['error'],
                           Error_Code.missing_bathrooms['error'],
                           Error_Code.missing_price['error'],
                           Error_Code.missing_description['error'],
                           Error_Code.missing_province['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_address['error'],
                           Error_Code.missing_image['error'],
                           Error_Code.missing_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        ###########################################################################

        # test case 4: there're some missing fields
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
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_sqft['error'],
                           Error_Code.missing_description['error'],
                           Error_Code.missing_city['error'],
                           Error_Code.missing_image['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ###########################################################################
        # test case 5
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
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.un_auth_listing['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        ###########################################################################
        # test case 6
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
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.invalid_user_id['error'],
                           Error_Code.un_auth_listing['error'],
                           Error_Code.invalid_bedrooms['error'],
                           Error_Code.invalid_sqft['error'],
                           Error_Code.invalid_bathrooms['error'],
                           Error_Code.invalid_price['error'],
                           Error_Code.invalid_thumbnail_image_index['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #############################################################################
        # test case 7: correct input
        # Note that the user along with the userId is created on melody's local host,
        # so it shouldn't be working on other computer


        # first, we need to create a user
        newUser = {"email": "student@usask.ca",
                  "password": "aaAA1234",
                  "firstName": "Student",
                  "lastName": "USASK",
                  "city": "Saskatoon",
                  "postalCode": "S7N 4P7",
                  "province": "Saskatchewan",
                  "phone1": 1111111111,
                  "confirmedPassword": "aaAA1234"
                  }

        request = webapp2.Request.blank('/createuser', POST=newUser)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        # now we can create a listing using the userId that just returned back from the new created user
        input = {"userId": output['userId'],
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
        input["userId"] = output["userId"]
        request = webapp2.Request.blank('/createlisting', POST=input)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 200)

        output = json.loads(response.body)
        self.assertTrue("listingId" in output)

        listing_created = Listing.get_by_id(output["listingId"])
        self.assertEquals(listing_created.bedrooms, 2)
        self.assertEquals(listing_created.sqft, 1200)
        self.assertEquals(listing_created.bathrooms, 2)
        self.assertEquals(listing_created.price, 200000)
        self.assertEquals(listing_created.description, "This is a nice house")
        self.assertEquals(listing_created.isPublished, True)
        self.assertEquals(listing_created.province, "Saskatchewan")
        self.assertEquals(listing_created.city, "Saskatoon")
        self.assertEquals(listing_created.address, "91 Campus Dr.")
        self.assertEquals(listing_created.thumbnailImageIndex, 0)
        self.assertEquals(listing_created.images, 'some images')




    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()




def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
