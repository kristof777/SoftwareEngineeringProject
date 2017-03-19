import sys
from extras.Utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
from API_NAME import get_favourites_listing_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")


class GetFavourites(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  do nothing
    Post:
        @pre-cond: Expecting keys to be userId
        @post-cond: favorite listings that are published
    """
    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        self.response.out.write()

    def post(self):
        setup_post(self.response)
        valid, values = \
            check_required_valid(get_favourites_listing_api,
                                 self.request.POST, self.response, True)

        if not valid:
            return
        # Get all favorites object that satisfies the filter condition
        favorites = Favorite.query(Favorite.userId == int(values['userId']),
                                   Favorite.liked == True).fetch()

        returned_array = []
        for favorite in favorites:
            fav_listingId = favorite.listingId
            listing = Listing.get_by_id(fav_listingId)
            assert listing is not None
            if listing.isPublished:
                template_values = {
                    'listingId': fav_listingId,
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
                    'images': listing.images,
                    'longitude': listing.longitude,
                    'latitude': listing.latitude,
                    'postalCode': listing.postalCode,
                    'thumbnailImageIndex': listing.thumbnailImageIndex
                }
                returned_array.append(template_values)

        write_success_to_response(self.response, {"listings": returned_array})
