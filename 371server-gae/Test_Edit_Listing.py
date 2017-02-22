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

    def test_edit_listing(self):

        # first of all, we need to create an owner, a listing that belongs to the owner, and an editor

        owner = {"email": "student@usask.ca",
                   "password": "aaAA1234",
                   "firstName": "Student",
                   "lastName": "USASK",
                   "city": "Saskatoon",
                   "postalCode": "S7N 4P7",
                   "province": "Saskatchewan",
                   "phone1": 1111111111,
                   "confirmedPassword": "aaAA1234"
                   }

        request = webapp2.Request.blank('/createuser', POST=owner)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        ownerId = output['userId']

        listing = {"userId": ownerId,
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
        request = webapp2.Request.blank('/createlisting', POST=listing)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        listingId = output["listingId"]

        editor = {"email": "editor@usask.ca",
                 "password": "Ycd245577",
                 "firstName": "Student",
                 "lastName": "EDT",
                 "city": "Regina",
                 "postalCode": "R7N 4P7",
                 "province": "Saskatchewan",
                 "phone1": 222222222222,
                 "confirmedPassword": "Ycd245577"
                 }

        request = webapp2.Request.blank('/createuser', POST=editor)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        editorId = output["userId"]


        #############################################################################################3
        # test case 1: missing input
        emptyInput = {}

        request = webapp2.Request.blank('/editListing', POST=emptyInput)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_listing_id['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #################################################################################################
        # test case 2: missing key-value pair
        wrongPairInput = {
            "province": "",
            "city": "   ",
            "bathrooms": "",
            "description": "  ",
            "userId": "",
            "listingId": ""
        }

        request = webapp2.Request.blank('/editListing', POST=wrongPairInput)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_listing_id['error'],
                           Error_Code.nothing_requested_to_change['error'], # province
                           Error_Code.nothing_requested_to_change['error'], # city
                           Error_Code.nothing_requested_to_change['error'], # bathrooms
                           Error_Code.nothing_requested_to_change['error']] # description

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #################################################################################################
        # test case 3: unrecognized key

        wrongKeyInput = {
            "blablabla": "blablabla",
            "userId": ownerId,
            "listingId": listingId
        }
        request = webapp2.Request.blank('/editListing', POST=wrongKeyInput)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.unrecognized_key['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

        #################################################################################################
        # test case 4: the editor, which is not the owner, cannot edit the listing

        wrongPersonInput = {
            "listingId": listingId,
            "userId": editorId,
            "bathrooms": 10
        }

        request = webapp2.Request.blank('/editListing', POST=wrongPersonInput)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.not_authorized['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        #################################################################################################
        # test case 5: invalid userId and listingId

        invalidInput = {
            "listingId": "blablabla",
            "userId": "blablabla",
            "bathrooms": 10
        }

        request = webapp2.Request.blank('/editListing', POST=invalidInput)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.invalid_user_id['error'],
                           Error_Code.invalid_listing_id['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        #################################################################################################
        # test case 6: unauthorized userId and listingId

        unauthorizedInput = {
            "listingId": 1111111,
            "userId": 4444444,
            "bathrooms": 10
        }

        request = webapp2.Request.blank('/editListing', POST=unauthorizedInput)  # api you need to test
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.not_authorized['error'],
                           Error_Code.un_auth_listing['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ################################################################################################
        # test case 7: input with invalid fields

        invalidFieldInput = {"userId": ownerId,
                        "listingId": listingId,
                        "bedrooms": "supposed to be a number",
                        "sqft": "supposed to be a number",
                        "bathrooms": "supposed to be a number",
                        "price": "supposed to be a number",
                        "isPublished": "supposed to be a boolean",
                        "city": "Regina",
                        "address": "312 Summer Place",
                        "thumbnailImageIndex": "supposed to be a number"
                        }
        request = webapp2.Request.blank('/editListing', POST=invalidFieldInput)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.invalid_bedrooms['error'],
                           Error_Code.invalid_sqft['error'],
                           Error_Code.invalid_bathrooms['error'],
                           Error_Code.invalid_price['error'],
                           Error_Code.invalid_thumbnail_image_index['error'],
                           Error_Code.invalid_published['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)



        #################################################################################################
        # test case 8: correct input

        correctInput = {"userId": ownerId,
                     "listingId": listingId,
                     "bedrooms": "4",
                     "sqft": "1500",
                     "bathrooms": "5",
                     "price": "2050000",
                     "isPublished": "False",
                     "city": "Regina",
                     "address": "312 Summer Place",
                     "thumbnailImageIndex": 1
                 }
        request = webapp2.Request.blank('/editListing', POST=correctInput)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        listing_changed = Listing.get_by_id(listingId)
        self.assertEquals(listing_changed.bedrooms, 4)
        self.assertEquals(listing_changed.sqft, 1500)
        self.assertEquals(listing_changed.bathrooms, 5)
        self.assertEquals(listing_changed.price, 2050000)
        self.assertEquals(listing_changed.description, "This is a nice house")
        self.assertEquals(listing_changed.isPublished, False)
        self.assertEquals(listing_changed.province, "Saskatchewan")
        self.assertEquals(listing_changed.city, "Regina")
        self.assertEquals(listing_changed.address, "312 Summer Place")
        self.assertEquals(listing_changed.thumbnailImageIndex, 1)
        self.assertEquals(listing_changed.images, 'some images')



    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()

def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
