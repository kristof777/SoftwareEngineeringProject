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


    def test_get_fav_listings(self):


        # first, we need to create a user as the owner of several listings
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

        # now we can create a few listings using the userId that just returned back from the new created user
        newListing1 = {"userId": ownerId,
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


        request = webapp2.Request.blank('/createlisting', POST=newListing1)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        listingId1 = output["listingId"]


        # listing 2
        newListing2 = {"userId": ownerId,
                      "bedrooms": "4",
                      "sqft": "1000",
                      "bathrooms": "4",
                      "price": "250000",
                      "description": "Get this nice house today!",
                      "isPublished": "False",
                      "province": "Saskatchewan",
                      "city": "Regina",
                      "address": "312 Summer Place",
                      "thumbnailImageIndex": 0,
                      "images": 'some images'
                      }


        request = webapp2.Request.blank('/createlisting', POST=newListing2)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        listingId2 = output["listingId"]

        # listing 3
        newListing3 = {"userId": ownerId,
                       "bedrooms": "1",
                       "sqft": "11000",
                       "bathrooms": "1",
                       "price": "1110000",
                       "description": "Move in today!",
                       "isPublished": "True",
                       "province": "BC",
                       "city": "Vancouver",
                       "address": "32 Redeer St.",
                       "thumbnailImageIndex": 0,
                       "images": 'some images'
                       }

        request = webapp2.Request.blank('/createlisting', POST=newListing3)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)

        listingId3 = output["listingId"]



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


        # liker likes these three listings
        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = likerId
        likeTheListing["listingId"] = listingId1

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = likerId
        likeTheListing["listingId"] = listingId2

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)

        likeTheListing = {
            "userId": "",
            "listingId": "",
            "liked": "True"
        }

        likeTheListing["userId"] = likerId
        likeTheListing["listingId"] = listingId3

        request = webapp2.Request.blank('/like', POST=likeTheListing)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)


        #######################################################################3
        # test case 1: successful get info

        getFavs = {
            "userId": likerId
        }

        request = webapp2.Request.blank('/getFavoriteListing', POST=getFavs)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        print response.body





    def tearDown(self):
        # Don't forget to deactivate the testbed after the tests are
        # completed. If the testbed is not deactivated, the original
        # stubs will not be restored.
        self.testbed.deactivate()

def run_tests():
    unittest.main()

if __name__ == "__main__":
    run_tests()
