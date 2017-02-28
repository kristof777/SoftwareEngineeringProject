import sys
sys.path.append("../")
from models.Listing import Listing
from models.User import User
import sys
sys.path.append("../")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.utils import *
import datetime


class EditListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        error_keys = ['changeValues', 'userId', 'listingId']
        errors, values = keys_missing(error_keys, self.request.POST)

        if len(errors) != 0:
            write_error_to_response(self.response,
                                    errors, missing_invalid_parameter_error)
            return

        change_values = json.loads(values['changeValues'])
        if len(change_values) == 0:
            write_error_to_response(self.response, {nothing_requested_to_change['error']:
                                                        "Nothing requested to change"},
                                                 nothing_requested_to_change['status'])
            return


        if any(key not in ["sqft", "bedrooms", "bathrooms", "price", "city",
                "province", "address", "description", "isPublished", "images",
                "thumbnailImageIndex"] for key in change_values.keys()):
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
        change_error_keys = []
        for change_key in change_values:
            change_error_keys.append(change_key)
        change_errors, change_fields = keys_missing(change_error_keys, change_values)
        if len(change_errors) != 0:
            write_error_to_response(self.response,
                                    change_errors, missing_invalid_parameter_error)
            return

        # check invalidity

        invalid = key_validation(values)    # the whole dictionary
        invalid.update(key_validation(change_values))   # the change_values dictionary


        if len(invalid) != 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter_error)
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

        userId = int(values['userId'])

        # make sure that the userId is the owner id of the listing
        listingOwnerId = listing.userId
        if listingOwnerId != userId:
            error = {
                not_authorized['error']: "Provided user ID doesn't match the owner id of the listing"
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        for key in change_values:
            listing.set_property(key, change_values[key])

        write_success_to_response(self.response, {'modifiedDate': str(datetime.datetime.now())})





