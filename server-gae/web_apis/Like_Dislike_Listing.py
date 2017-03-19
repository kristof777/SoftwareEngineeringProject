import os
from extras.Utils import *
from models.Favorite import Favorite
from models.Listing import Listing
from models.User import User
import sys
from API_NAME import like_listing_api
from extras.Required_Fields import check_required_valid
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class LikeDislikeListing(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be listingId, userId and liked. If any
                   of these is not present an appropriate error and
                   status code 400 is returned.

                   listingId and userId are supposed to be integers, and liked
                   is either "True" or "False".
        @post-cond: A favorite object with provided listingId and userId is created in the
                    database if it doesn't exist before, or update the liked field if it exists.
                    Return nothing.
    """

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):

        self.render_template('../webpages/Like_dislike_listing.html')

    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(like_listing_api, self.request.POST,
                                 self.response)

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

        liked = convert_to_bool(values['liked'])
        user_id = int(values['userId'])
        listing_id = int(values['listingId'])

        # make sure that the owner can't like his/her own listing
        listing_owner_id = listing.userId
        if listing_owner_id == user_id:
            error = {
                unallowed_liked['error']: 'Listing can\'t be liked by owner'
            }
            write_error_to_response(self.response, error,
                                    processing_failed)
            return

        # check if the favorite object exists
        favorite = Favorite.query(Favorite.userId == user_id,
                                  Favorite.listingId == listing_id).get()
        if favorite is None:
            favorite = Favorite(userId=user_id, listingId=listing_id, liked=liked)
            favorite.put()
        else:  # if the favorite object does exist
            favorite_liked = favorite.liked
            if liked:
                # user want to like the list
                if favorite_liked:
                    # return duplicate error
                    error = {
                        duplicated_liked['error']: 'The listing is already liked'
                    }
                    write_error_to_response(self.response, error,
                                            processing_failed)
                    return

                # if everything is correct, change the liked field to be true
                favorite.liked = True

            else:
                # user want to unlike the list
                if not favorite_liked:
                    # return error
                    error = {
                        duplicated_liked['error']: 'The listing is already disliked'
                    }
                    write_error_to_response(self.response, error,
                                            processing_failed)
                    return

                # change the liked field to be false
                favorite.liked = False
            favorite.put()

        # return successfully
        write_success_to_response(self.response, {})
