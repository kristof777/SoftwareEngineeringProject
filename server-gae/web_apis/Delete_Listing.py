import os
from extras.utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
import sys
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class DeleteListing(webapp2.RequestHandler):

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

        error_keys = ['userId', 'listingId', 'authToken']

        errors,values = keys_missing(error_keys, self.request.POST)

        # If there exists error then return the response, and stop the function
        # if not, then go ahead and check validity
        if len(errors) != 0:
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter)
            return

        # check validity for integer fields (userId and listingId) and a boolean field (isPublished)
        invalid = key_validation(values)

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid,
                                    missing_invalid_parameter)
            return

        # find the correct user with userId
        user = User.get_by_id(int(values['userId']))
        if user is None:
            error = {
                not_authorized['error']: 'User not authorized'
            }
            write_error_to_response(self.response, error,
                                    unauthorized_access)
            return

        # Check if it is the valid user
        valid_user = user.validate_token(int(values["userId"]),
                                         "auth",
                                         values["authToken"])
        if not valid_user:
            write_error_to_response(self.response, {not_authorized['error']:
                                                        "not authorized to delete listings"},
                                    not_authorized['status'])
            return

        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: 'Listing not authorized'
            }
            write_error_to_response(self.response, error,
                                    unauthorized_access)
            return

        user_id = int(values['userId'])
        listing_id = int(values['listingId'])

        # make sure that the userId is the owner id of the listing
        listing_owner_id = listing.userId
        if listing_owner_id != user_id:
            error = {
                not_authorized[
                    'error']: "Provided user ID doesn't match the owner id of the listing"
            }
            write_error_to_response(self.response, error, unauthorized_access)
            return

        # delete all favorites related to this listing
        favorites = Favorite.query(Favorite.listingId == listing_id).fetch()
        if favorites:
            for favorite in favorites:
                favorite.key.delete()

        # delete the listing itself
        listing.key.delete()

        # return successfully
        write_success_to_response(self.response, {})




























