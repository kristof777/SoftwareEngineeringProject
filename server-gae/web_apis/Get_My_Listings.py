import sys
from extras.Utils import *
from models.Listing import Listing
from models.User import User
from API_NAME import get_messages_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")


class GetMyListing(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  do nothing
    Post:
        @pre-cond: Expecting keys to be userId
        @post-cond: all my listings
    """
    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        self.response.out.write()

    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(get_messages_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        owner_id = int(values['userId'])

        my_listings = Listing.query(Listing.userId == owner_id).fetch()
        returned_array = []

        for listing in my_listings:
            template_values = {
                'listingId': listing.listingId,
                'userId': listing.userId,
                'bedrooms': listing.bedrooms,
                'squareFeet': listing.squareFeet,
                'bathrooms': listing.bathrooms,
                'price': listing.price,
                'description': listing.description,
                'isPublished': listing.isPublished,
                'province': listing.province,
                'city': listing.city,
                'address': listing.address,
                'longitude': listing.longitude,
                'latitude': listing.latitude,
                'images': listing.images,
                'thumbnailImageIndex': listing.thumbnailImageIndex,
                'postalCode': listing.postalCode
            }
            returned_array.append(template_values)

        write_success_to_response(self.response, {"listings": returned_array})
