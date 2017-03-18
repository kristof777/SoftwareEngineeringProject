import os
from extras.utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
import sys
from API_NAME import delete_listing_api
from extras.api_required_fields import check_required_valid
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class DeleteListing(webapp2.RequestHandler):

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        self.response.out.write()

    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(delete_listing_api, self.request.POST,
                                 self.response, True)

        if not valid:
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




























