from extras.utils import *
import datetime
from models.Listing import Listing
from models.User import User
import sys
import os
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class EditListing(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: the listing object should exist
                   listingId and userId are supposed to be integers,
                   valuesRequired should be a dictionary
        @post-cond: a timestamp of modified date should be returned
    """
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        # check if there's any missing field, if so, just return to the user what all is missing
        error_keys = ['changeValues', 'userId', 'listingId']
        errors, values = keys_missing(error_keys, self.request.POST)

        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            write_error_to_response(self.response,
                                    errors, missing_invalid_parameter)
            return

        # check if "changeValues" is empty
        if len(values['changeValues']) == 0:
            write_error_to_response(self.response,
                                    {nothing_requested_to_change['error']:
                                         "Nothing requested to change"},
                                    nothing_requested_to_change['status'])
            return

        change_values = json.loads(values['changeValues'])

        # check if there's any unrecognized key presented in changeValues
        if any(key not in ["sqft", "bedrooms", "bathrooms", "price", "city",
                           "province", "address", "description", "isPublished",
                           "images","thumbnailImageIndex"] for key in
               change_values.keys()):
            write_error_to_response(self.response, {unrecognized_key['error']:
                                                        "Unrecognized key found"},
                                    unrecognized_key['status'])
            return

        # In order to detect empty field in changeValues keys
        # for example,
        # wrongPairInput = {
        #     "changeValues": {
        #         "province": "",
        #         "city": "   ",
        #         "bathrooms": "",
        #         "description": "  ",
        #     },
        #     "userId": "",
        #     "listingId": ""
        # }
        # we need to go through each field in the dictionary
        change_error_keys = []
        for change_key in change_values:
            change_error_keys.append(change_key)
        change_errors, change_fields = keys_missing(change_error_keys,
                                                    change_values)
        if len(change_errors) != 0:
            write_error_to_response(self.response,
                                    change_errors,
                                    missing_invalid_parameter)
            return

        # check invalidity
        invalid = key_validation(values)  # the whole dictionary
        invalid.update(
            key_validation(change_values))  # the change_values dictionary

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter)
            return

        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: "Listing not authorized"
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        user_id = int(values['userId'])

        # make sure that the userId is the owner id of the listing
        listing_owner_id = listing.userId
        if listing_owner_id != user_id:
            error = {
                not_authorized[
                    'error']: "Provided user ID doesn't match the owner id of the listing"
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        for key in change_values:
            listing.set_property(key, change_values[key])
        listing.put()
        write_success_to_response(self.response, {
            'modifiedDate': str(datetime.datetime.now())})
