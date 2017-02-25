from __future__ import absolute_import
import unittest
import json
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import extras.Error_Code as Error_Code
import Main
import webapp2
from google.appengine.ext import testbed
from models.Listing import Listing
from web_apis.Create_User import *
import extras.utils as utils


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


    def test_get_my_listings(self):
        # first, we need to create a user as the owner of several listings
        owner = {"email": "student@usask.ca",
                 "password": "aaAA12345",
                 "firstName": "Student",
                 "lastName": "USASK",
                 "city": "Saskatoon",
                 "postalCode": "S7N 4P7",
                 "province": "Saskatchewan",
                 "phone1": 1111111111,
                 "confirmedPassword": "aaAA12345"
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


        #######################################################################3
        # test case 1: successful get info


        getMyListings = {
            "userId": ownerId
        }

        request = webapp2.Request.blank('/getMyListing', POST=getMyListings)
        response = request.get_response(Main.app)
        self.assertEquals(response.status_int, 200)
        output = json.loads(response.body)
        self.assertEquals(len(output["myListings"]), 3)

        listing1 = output["myListings"][0]

        self.assertEquals(listing1['province'], newListing1['province'])
        self.assertEquals(listing1['city'], newListing1['city'])
        self.assertEquals(listing1['address'], newListing1['address'])
        self.assertEquals(listing1['bathrooms'], int(newListing1['bathrooms']))
        self.assertEquals(listing1['sqft'], int(newListing1['sqft']))
        self.assertEquals(listing1['bedrooms'], int(newListing1['bedrooms']))
        self.assertEquals(listing1['price'], int(newListing1['price']))
        self.assertEquals(listing1['description'], newListing1['description'])
        self.assertEquals(str(listing1['isPublished']), newListing1['isPublished'])
        self.assertEquals(listing1['thumbnailImageIndex'], int(newListing1['thumbnailImageIndex']))
        self.assertEquals(listing1['userId'], int(newListing1['userId']))
        self.assertEquals(listing1['listingId'], int(listingId1))

        listing2 = output["myListings"][1]

        self.assertEquals(listing2['province'], newListing2['province'])
        self.assertEquals(listing2['city'], newListing2['city'])
        self.assertEquals(listing2['address'], newListing2['address'])
        self.assertEquals(listing2['bathrooms'], int(newListing2['bathrooms']))
        self.assertEquals(listing2['sqft'], int(newListing2['sqft']))
        self.assertEquals(listing2['bedrooms'], int(newListing2['bedrooms']))
        self.assertEquals(listing2['price'], int(newListing2['price']))
        self.assertEquals(listing2['description'], newListing2['description'])
        self.assertEquals(str(listing2['isPublished']), newListing2['isPublished'])
        self.assertEquals(listing2['thumbnailImageIndex'], int(newListing2['thumbnailImageIndex']))
        self.assertEquals(listing2['userId'], int(newListing2['userId']))
        self.assertEquals(listing2['listingId'], int(listingId2))

        listing3 = output["myListings"][2]

        self.assertEquals(listing3['province'], newListing3['province'])
        self.assertEquals(listing3['city'], newListing3['city'])
        self.assertEquals(listing3['address'], newListing3['address'])
        self.assertEquals(listing3['bathrooms'], int(newListing3['bathrooms']))
        self.assertEquals(listing3['sqft'], int(newListing3['sqft']))
        self.assertEquals(listing3['bedrooms'], int(newListing3['bedrooms']))
        self.assertEquals(listing3['price'], int(newListing3['price']))
        self.assertEquals(listing3['description'], newListing3['description'])
        self.assertEquals(str(listing3['isPublished']), newListing3['isPublished'])
        self.assertEquals(listing3['thumbnailImageIndex'], int(newListing3['thumbnailImageIndex']))
        self.assertEquals(listing3['userId'], int(newListing3['userId']))
        self.assertEquals(listing3['listingId'], int(listingId3))

        #######################################################################3
        # test case 2: invalid userId

        invalidMyListings = {
            "userId": "blablabla"
        }

        request = webapp2.Request.blank('/getMyListing', POST=invalidMyListings)
        response = request.get_response(Main.app)

        self.assertEquals(response.status_int, 400)

        errors_expected = [Error_Code.invalid_user_id['error']]

        error_keys = [str(x) for x in json.loads(response.body)]

        # checking if there is a difference between error_keys and what we got
        self.assertEquals(len(set(errors_expected).
                              difference(set(error_keys))), 0)

