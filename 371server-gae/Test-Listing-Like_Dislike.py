import json
import os
import unittest

import Error_Code
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

        # test case 1: correct input

        # first, we need to create a user
        newUser = {"email": "student@usask.ca",
                   "password": "123456",
                   "firstName": "Student",
                   "lastName": "USASK",
                   "city": "Saskatoon",
                   "postalCode": "S7N 4P7",
                   "province": "Saskatchewan",
                   "phone1": 1111111111,
                   "confirmedPassword": "123456"
                 }

        request = webapp2.Request.blank('/createuser', POST=newUser)  # api you need to test
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        userId = output["userId"]



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

        newListing["userId"] = userId

        request = webapp2.Request.blank('/createlisting', POST=newListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        listingId = output["listingId"]



        # now user want to like the listing
        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = userId
        likeTheListing["listingId"] = listingId

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

















    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest.main()
