import json
import os
import sys
sys.path.append("../")
import webapp2
from google.appengine.ext.webapp import template
import extras.Error_Code as Error_Code
from models.Listing import Listing
from models.User import User
from models.Favorite import Favorite
from extras.utils import *





class GetFavoriteListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['userId']

        # check if there's any missing field, if so, just return to the user what all is missing
        # if not, then go ahead and check validity

        errors, values = keys_missing(error_keys, self.request.POST)

        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            write_error_to_response(self.response, errors, missing_invalid_parameter_error)
            return

        # check validity for integer fields (userId, bedrooms, bathrooms, sqft, price, thumbnailImageIndex)
        #  and boolean field (isPublished)
        invalid = key_validation(values)

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter_error)
            return

        # find the correct user with userId
        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            write_error_to_response(self.response, error, missing_invalid_parameter_error)
            return

        favorites = Favorite.query(Favorite.userId == int(values['userId']), Favorite.liked == True).fetch()

        returnedArray = []
        for favorite in favorites:

            favListingId = favorite.listingId
            listing = Listing.get_by_id(favListingId)

            if listing.isPublished:
                template_values = {
                    'listingId': listing.listingId,
                    'userId': listing.userId,
                    'bedrooms': listing.bedrooms,
                    'sqft': listing.sqft,
                    'bathrooms': listing.bathrooms,
                    'price': listing.price,
                    'description': listing.description,
                    'isPublished': listing.isPublished,
                    'province': listing.province,
                    'city': listing.city,
                    'address': listing.address,
                    'images': listing.images,
                    'thumbnailImageIndex': listing.thumbnailImageIndex
                }
                returnedArray.append(template_values)

        write_success_to_response(self.response, {"listings": returnedArray})
