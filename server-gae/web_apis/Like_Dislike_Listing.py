import sys
sys.path.append("../")
from models.Favorite import Favorite
import sys
sys.path.append("../")
from models.Listing import Listing
from models.User import User
import sys
sys.path.append("../")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.utils import *



class LikeDislikeListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):

        self.render_template('../webpages/Like_dislike_listing.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        error_keys = ['userId', 'listingId', 'liked']

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

        listing = Listing.get_by_id(int(values['listingId']))
        if listing is None:
            error = {
                un_auth_listing['error']: 'Listing not authorized'
            }
            write_error_to_response(self.response, error, missing_invalid_parameter_error)
            return

        if values['liked'] == "True":
            liked = True
        else:
            liked = False

        userId = int(values['userId'])
        listingId = int(values['listingId'])


        # make sure that the owner can't like his/her own listing
        listingOwnerId = listing.userId
        if listingOwnerId == userId:
            error = {
                unallowed_liked['error']: 'Listing can\'t be liked by owner'
            }
            write_error_to_response(self.response, error, missing_invalid_parameter_error)
            return

        # Next, check if the favorite object already exists
        # if it already exists, check the user input liked
        #   if liked == true, then it means the user want to like the list
        #       if the liked field in the object is true, return error
        #       if the liked field in the object is false, change it to true
        #   if liked == false, then it means the user want to unlike the list
        #       if the liked field in the object is false, then return error
        #       if the liked field in the object is true, change it to false
        # if the favorite object doesn't exist
        #   create a new favorite object with liked input value


        # check if the favorite object exists
        favorite = Favorite.query(Favorite.userId == userId, Favorite.listingId == listingId).get()
        if favorite is None:
            # TODO: do we need to make sure that the liked input is true when creating the favorite object?
            favorite = Favorite(userId=userId, listingId=listingId, liked=liked)
            favorite.put()
        else:  # if the favorite object does exist
            favoriteLiked = favorite.liked
            if liked:
                # user want to like the list
                if favoriteLiked:
                    # return duplicate error
                    error = {
                        duplicated_liked['error']: 'The listing is already liked'
                    }
                    write_error_to_response(self.response, error, missing_invalid_parameter_error)
                    return

                # if everything is correct, change the liked field to be true
                favorite.liked = True

            else:
                # user want to unlike the list
                if not favoriteLiked:
                    # return error
                    error = {
                        duplicated_liked['error']: 'The listing is already disliked'
                    }
                    write_error_to_response(self.response, error, missing_invalid_parameter_error)
                    return

                # change the liked field to be false
                favorite.liked = False

            # return successfully
            write_success_to_response(self.response, {})

