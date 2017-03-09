from models.Listing import Listing
from models.User import User
import sys
import os
from extras.utils import *
sys.path.append("../")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


class CreateListing(webapp2.RequestHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be price, sqft, bedrooms,
                   bathrooms, description, images, thumbnailImageIndex,
                   city, address, province, userId, isPublished. If any
                   of these is not present an appropriate error and
                   status code 400 is returned.

                   There's a few fields which are supposed to be integer:
                   bedrooms, sqft, price, userId and thumbnailImageIndex;
                   There's a field that's supposed to be a float: bathrooms;
                   There's a field that's supposed to be a bool: isPublished
        @post-cond: A listing with provided information is created in the
                    database. ListingId is returned as an response
                    object.

    """
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers[
            'Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    # this GET method is only used for the testing browser
    def get(self):
        self.render_template('../webpages/Create_Listing.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = listing_keys

        # check if there's any missing field, if so, just return to the user what all is missing
        errors, values = keys_missing(error_keys, self.request.POST)

        # If there exists error then return the response, and stop the function
        # if not, then go ahead and check validity
        if len(errors) != 0:
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter)
            return

        # check validity for integer fields (userId, bedrooms, bathrooms, sqft, price, thumbnailImageIndex)
        #  and boolean field (isPublished)
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
                                                        "not authorized to create listings"},
                                    not_authorized['status'])
            return

        values['province'] = scale_province(str(values['province']))
        is_published = convert_to_bool(values["isPublished"])

        # all set
        values['images'] = json.loads(values['images'])
        values['images'] = [str(image) for image in values['images']]
        listing = Listing(userId=int(values['userId']),
                          bedrooms=int(values['bedrooms']),
                          squarefeet=int(values['squarefeet']),
                          bathrooms=float(values['bathrooms']),
                          price=int(values['price']),
                          description=values['description'],
                          isPublished=is_published, province=values['province'],
                          city=values['city'],
                          address=values['address'], images=values['images'],
                          longitude=float(values['longitude']),
                          latitude=float(values['latitude']),
                          thumbnailImageIndex=int(
                              values['thumbnailImageIndex']))
        listing.put()
        listing.set_property('listingId', listing.key.id())
        listing.put()
        write_success_to_response(self.response,
                                  {'listingId': listing.listingId})
