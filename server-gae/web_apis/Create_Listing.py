import json
import os
import sys
sys.path.append("../")
from models.Listing import Listing
from models.User import User
import sys
sys.path.append("../")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.utils import *


# The GET method is simply get the html page ( in the browser for back-end testing)
# for user inputs. The POST method is similar to create_user, what it does is to get
# all the information from what the user typed, and generate a new listing that belongs
# to the current user (with email as the key).
class CreateListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    # this GET method is only used for the testing browser
    def get(self):
        self.render_template('../webpages/Create_Listing.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['price', 'sqft', 'bedrooms', 'bathrooms', 'description', 'images',
                      'thumbnailImageIndex', 'address', 'province', 'city', 'userId', 'isPublished']

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
                un_auth_listing['error']: 'listing unauthorized'
            }
            write_error_to_response(self.response, error, missing_invalid_parameter_error)
            return

        values['province'] = scale_province(str(values['province']))

        if values['isPublished'] == "True":
            isPublished = True
        else:
            isPublished = False

        # all set
        listing = Listing(userId=int(values['userId']), bedrooms=int(values['bedrooms']), sqft=int(values['sqft']),
                          bathrooms=float(values['bathrooms']), price=int(values['price']), description=values['description'],
                          isPublished=isPublished, province=values['province'], city=values['city'],
                          address=values['address'], images=values['images'],
                          thumbnailImageIndex=int(values['thumbnailImageIndex']))
        listing.put()
        listing.setProperty('listingId', listing.key.id())
        write_success_to_response(self.response, {'listingId': listing.listingId})
