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
    GetFavourites class is used to respond to request to getFavourites api.
    The post method in this class is used to get all the listings liked by
    the user.
    Post:
        @pre-cond: Expecting keys to be userId and authToken.
                   User with provided userId should be present in the database.
                   authToken should be valid for given userId.
        @post-cond: Nothing
        @return-api: All the listing liked by the user with userId are returned.
    """

    def options(self, *args, **kwargs):
        setup_api_options(self)

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
