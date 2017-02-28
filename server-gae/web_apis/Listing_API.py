import json
import os
import sys
sys.path.append("../")
import webapp2
from google.appengine.ext.webapp import template
import extras.Error_Code as Error_Code
from models.Listing import Listing
from models.User import User
from models.Favorite import Favorite


# class EditListing(webapp2.RequestHandler):
#     def options(self, *args, **kwargs):
#         self.response.headers['Access-Control-Allow-Origin'] = '*'
#         self.response.headers[
#             'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
#         self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
#
#     def get(self):
#         self.response.out.write()
#
#     def post(self):
#         self.response.headers.add_header('Access-Control-Allow-Origin', '*')
#         errors = {}
#         emptyData = u''
#
#         requestUserId = self.request.POST.get('userId')
#         if requestUserId is emptyData or requestUserId is None or requestUserId.isspace():
#             errors[Error_Code.missing_user_id['error']] = "UserId not provided"
#
#         requestListingId = self.request.POST.get('listingId')
#         if requestListingId is emptyData or requestListingId is None or requestListingId.isspace():
#             errors[Error_Code.missing_listing_id['error']] = "ListingId not provided"
#
#
#         for key, value in self.request.POST.items():
#             if value is emptyData or value is None or value.isspace():
#                 errors[Error_Code.nothing_requested_to_change['error']] = "There was no value for key " + key
#             if key != 'bedrooms' \
#                 and key != 'bathrooms' \
#                 and key != 'province' \
#                 and key != 'sqft' \
#                 and key != 'price' \
#                 and key != 'description' \
#                 and key != 'isPublished' \
#                 and key != 'city' \
#                 and key !='images' \
#                 and key != 'thumbnailImageIndex'\
#                 and key != 'address' \
#                 and key != 'userId' \
#                 and key != 'listingId':
#                 errors[Error_Code.unrecognized_key['error']] = "Unknown key " + key
#
#
#         if len(errors) != 0:
#             error_json = json.dumps(errors)
#             self.response.write(error_json)
#             self.response.set_status(Error_Code.missing_invalid_parameter_error)
#             return
#
#         else:
#             try:
#                 requestUserId = int(requestUserId)
#             except:
#                 errors[Error_Code.invalid_user_id['error']] = "UserId not valid"
#
#             user = User.get_by_id(requestUserId)
#             if user is None:
#                 errors[Error_Code.not_authorized['error']] = "User not authorized"
#
#             userId = requestUserId
#
#             try:
#                 requestListingId = int(requestListingId)
#             except:
#                 errors[Error_Code.invalid_listing_id['error']] = "ListingId not valid"
#
#             listing = Listing.get_by_id(requestListingId)
#             if listing is None:
#                 errors[Error_Code.un_auth_listing['error']] = "Listing not authorized"
#
#             listingId = requestListingId
#
#             if len(errors) != 0:
#                 error_json = json.dumps(errors)
#                 self.response.write(error_json)
#                 self.response.set_status(Error_Code.missing_invalid_parameter_error)
#                 return
#
#             else:
#
#                 # make sure that the userId is the owner id of the listing
#                 listingOwnerId = listing.userId
#                 if listingOwnerId != userId:
#                     errors[Error_Code.not_authorized['error']] = "Provided user ID doesn't match the owner id of the listing"
#                     error_json = json.dumps(errors)
#                     self.response.write(error_json)
#                     self.response.set_status(Error_Code.missing_invalid_parameter_error)
#                     return
#
#                 # start changing values in the listing
#
#                 for key,value in self.request.POST.items():
#                     if key is not 'userId' and key is not 'listingId':
#                         errors.update(listing.setProperty(key, value))
#
#                 # invalid input
#                 if len(errors) != 0:
#                     error_json = json.dumps(errors)
#                     self.response.write(error_json)
#                     self.response.set_status(Error_Code.missing_invalid_parameter_error)
#                     return
#
#                 self.response.set_status(Error_Code.success)
#                 return
#
#
#


# class GetFavoriteListing(webapp2.RequestHandler):
#     def options(self, *args, **kwargs):
#         self.response.headers['Access-Control-Allow-Origin'] = '*'
#         self.response.headers[
#             'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
#         self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
#
#     def get(self):
#         self.response.out.write()
#
#     def post(self):
#         self.response.headers.add_header('Access-Control-Allow-Origin', '*')
#         errors = {}
#         emptyData = u''
#
#         likerId = self.request.POST.get('userId')
#         if likerId is emptyData or likerId is None or likerId.isspace():
#             errors[Error_Code.missing_user_id['error']] = "UserId not provided"
#         if len(errors) != 0:
#             error_json = json.dumps(errors)
#             self.response.write(error_json)
#             self.response.set_status(Error_Code.missing_invalid_parameter_error)
#             return
#
#         try:
#             likerId = int(likerId)
#         except:
#             errors[Error_Code.invalid_user_id['error']] = "UserId not valid"
#         if len(errors) != 0:
#             error_json = json.dumps(errors)
#             self.response.write(error_json)
#             self.response.set_status(Error_Code.missing_invalid_parameter_error)
#             return
#
#
#         favorites = Favorite.query(Favorite.userId == likerId, Favorite.liked == True).fetch()
#
#         returnedArray = []
#         for favorite in favorites:
#
#             favListingId = favorite.listingId
#             listing = Listing.get_by_id(favListingId)
#
#             if listing.isPublished:
#                 template_values = {
#                     'listingId': listing.listingId,
#                     'userId': listing.userId,
#                     'bedrooms': listing.bedrooms,
#                     'sqft': listing.sqft,
#                     'bathrooms': listing.bathrooms,
#                     'price': listing.price,
#                     'description': listing.description,
#                     'isPublished': listing.isPublished,
#                     'province': listing.province,
#                     'city': listing.city,
#                     'address': listing.address,
#                     'images': listing.images,
#                     'thumbnailImageIndex': listing.thumbnailImageIndex
#                 }
#                 returnedArray.append(template_values)
#
#         self.response.write(json.dumps({"listings": returnedArray}))
#         self.response.set_status(Error_Code.success)


class GetMyListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        self.response.out.write()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        errors = {}
        emptyData = u''

        ownerId = self.request.POST.get('userId')
        if ownerId is emptyData or ownerId is None or ownerId.isspace():
            errors[Error_Code.missing_user_id['error']] = "UserId not provided"
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        try:
            ownerId = int(ownerId)
        except:
            errors[Error_Code.invalid_user_id['error']] = "UserId not valid"
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        myListings = Listing.query(Listing.userId == ownerId).fetch()
        returnedArray = []

        for listing in myListings:
            template_values = {
                'listingId': listing.listingId,
                'userId': listing.userId,
                'bedrooms': listing.bedrooms,
                'sqft': listing.sqft,
                'bathrooms': listing.bathrooms,
                'price': listing.price,
                'description': listing.description,
                'isPublished': listing.isPublished,
                'province': listing.province,
                'city': listing.city,
                'address': listing.address,
                'images': listing.images,
                'thumbnailImageIndex': listing.thumbnailImageIndex
            }
            returnedArray.append(template_values)

        self.response.write(json.dumps({"myListings": returnedArray}))
        self.response.set_status(Error_Code.success)






