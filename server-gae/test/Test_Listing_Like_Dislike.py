from __future__ import absolute_import
import sys
sys.path.append("../")
import json
import os
import unittest
import extras.Error_Code as Error_Code
import Main
import webapp2
from google.appengine.ext import testbed
from models.Listing import Listing

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

    def test_like_dislike_a_listing(self):

        # first, we need to create a user as the owner of a listing
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

        ownerId = output["userId"]



        # now we can create a listing using the userId that just returned back from the new created user
        newListing = {"userId": "",
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

        newListing["userId"] = ownerId

        request = webapp2.Request.blank('/createlisting', POST=newListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        listingId = output["listingId"]



        # now create a new user as a liker
        liker = {"email": "like@usask.ca",
                   "password": "aaAA1234",
                   "firstName": "like",
                   "lastName": "liker",
                   "city": "Saskatoon",
                   "postalCode": "S7N 4P7",
                   "province": "Saskatchewan",
                   "phone1": 2222222222,
                   "confirmedPassword": "aaAA1234"
                 }

        request = webapp2.Request.blank('/createuser', POST=liker)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        likerId = output["userId"]




        #########################################################################################################
        # test case 1: the owner can't like their listings

        # now user want to like the listing
        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = ownerId
        likeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.unallowed_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        #####################################################################################################
        # test case 2: successful delivery (like the listing)

        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = likerId
        likeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)



        ########################################################################################################
        # test case 3: send a like request(liked==True) while the listing is already liked
        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = likerId
        likeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.duplicated_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ########################################################################################################
        # test case 4: dislike this listing
        # should be a successful delivery

        dislikeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "False"
        }

        dislikeTheListing["userId"] = likerId
        dislikeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=dislikeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)



        ########################################################################################################
        # test case 5: dislike this listing again
        dislikeTheListingAgain = {
            "userId": "",
            "listingId": "",
            "liked": "False"
        }

        dislikeTheListingAgain["userId"] = likerId
        dislikeTheListingAgain["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=dislikeTheListingAgain)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.duplicated_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ########################################################################################################
        # test case 6: missing user input

        likeWithMissingInput = {
            "userId": "",
            "listingId": "",
            "liked": ""
        }

        request = webapp2.Request.blank('/like', POST=likeWithMissingInput)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.missing_user_id['error'],
                           Error_Code.missing_listing_id['error'],
                           Error_Code.missing_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)


        ########################################################################################################
        # test case 7: invalid user input

        likeWithInvalidInput = {
            "userId": "supposed to be an integer",
            "listingId": "supposed to be an integer",
            "liked": "supposed to be a boolean"
        }

        request = webapp2.Request.blank('/like', POST=likeWithInvalidInput)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 400)
        errors_expected = [Error_Code.invalid_user_id['error'],
                           Error_Code.invalid_listing_id['error'],
                           Error_Code.invalid_liked['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)






    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
