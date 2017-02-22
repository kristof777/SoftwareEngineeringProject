import json
import os

import webapp2
from google.appengine.ext.webapp import template

import Error_Code
from models.Listing import Listing
from models.User import User
from models.Favorite import Favorite


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
        template_values = {
            # 'first_name': user2.first_name,
            # 'last_name': user2.last_name
        }
        # test = json.dumps(template_values)
        path = os.path.join(os.path.dirname(__file__), 'Create_Listing.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        emptyData = u''
        errors = {}

        # check if there's any missing field, if so, just return to the user what all is missing
        # if not, then go ahead and check validity
        requestUserId = self.request.POST.get('userId')
        if requestUserId is emptyData or requestUserId is None or requestUserId.isspace():
            errors[Error_Code.missing_user_id['error']] = "UserId not provided"

        bedrooms = self.request.POST.get('bedrooms')
        if bedrooms is emptyData or bedrooms is None or bedrooms.isspace():
            errors[Error_Code.missing_bedrooms['error']] = "Number of bedrooms not provided"

        sqft = self.request.POST.get('sqft')
        if sqft is emptyData or sqft is None or sqft.isspace():
            errors[
                Error_Code.missing_sqft['error']] = "Square feet not provided"

        bathrooms = self.request.POST.get('bathrooms')
        if bathrooms is emptyData or bathrooms is None or bathrooms.isspace():
            errors[Error_Code.missing_bathrooms['error']] = "Number of bathrooms not provided"

        price = self.request.POST.get('price')
        if price is emptyData or price is None or price.isspace():
            errors[Error_Code.missing_price['error']] = "Price not provided"

        description = self.request.POST.get('description')
        if description is emptyData or description is None or description.isspace():
            errors[Error_Code.missing_description['error']] = "Description not provided"

        isPublished = self.request.POST.get('isPublished')
        if isPublished is emptyData or isPublished is None or isPublished.isspace():
            errors[Error_Code.missing_published['error']] = "isPublished not provided"

        province = self.request.POST.get('province')
        if province is emptyData or province is None or province.isspace():
            errors[
                Error_Code.missing_province['error']] = "Province not provided"

        city = self.request.POST.get('city')
        if city is emptyData or city is None or city.isspace():
            errors[Error_Code.missing_city['error']] = "City not provided"

        address = self.request.POST.get('address')
        if address is emptyData or address is None or address.isspace():
            errors[Error_Code.missing_address['error']] = "Address not provided"

        images = str(self.request.POST.get('images'))
        if images is '' or images == 'None' or images.isspace():
            errors[Error_Code.missing_image['error']] = "Images not provided"

        thumbnailImageIndex = self.request.POST.get('thumbnailImageIndex')
        if thumbnailImageIndex is emptyData or thumbnailImageIndex is None or thumbnailImageIndex.isspace():
            errors[Error_Code.missing_image_index['error']] = "thumbnail not provided"

        # if there are missing fields, return
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(
                Error_Code.missing_invalid_parameter_error)
            return

        else:  # check validity for integer fields (userId, bedrooms, bathrooms, sqft, price, thumbnailImageIndex)

            try:
                requestUserId = int(requestUserId)
            except:
                errors[Error_Code.invalid_user_id['error']] = "UserId not valid"

            # find the correct user with userId
            user = User.get_by_id(requestUserId)
            if user is None:
                errors[Error_Code.un_auth_listing['error']] = "listing unauthorized"

            userId = requestUserId

            try:
                bedrooms = int(bedrooms)
            except:
                errors[Error_Code.invalid_bedrooms['error']] = "Number of bedrooms not valid"

            try:
                 sqft = int(sqft)
            except:
                errors[
                    Error_Code.invalid_sqft['error']] = "Square feet not valid"

            try:
                bathrooms = int(bathrooms)
            except:
                errors[Error_Code.invalid_bathrooms['error']] = "Number of bathrooms not valid"

            try:
                price = int(self.request.POST.get('price'))
            except:
                errors[Error_Code.invalid_price['error']] = "Price not valid"

            if isPublished != "True" and isPublished != "False":
                errors[Error_Code.invalid_published['error']] = "isPublished not valid"

            if isPublished == "True":
                isPublished = True
            else:
                isPublished = False

            try:
                thumbnailImageIndex = int(thumbnailImageIndex)
            except:
                errors[Error_Code.invalid_thumbnail_image_index['error']] = "Thumbnail image index not valid"


            if len(errors) != 0:    # if there is invalid fields
                error_json = json.dumps(errors)
                self.response.write(error_json)
                self.response.set_status(
                    Error_Code.missing_invalid_parameter_error)
                return
            else:
                # all set
                listing = Listing(userId=userId, bedrooms=bedrooms, sqft=sqft, bathrooms=bathrooms,
                                  price=price, description=description, isPublished=isPublished, province=province,
                                  city=city, address=address, images=images, thumbnailImageIndex=thumbnailImageIndex)
                listing.put()
                listing.listingId = listing.key.id()
                self.response.write(json.dumps({"listingId": listing.listingId}))
                self.response.set_status(Error_Code.success)

class LikeDislikeListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

    def get(self):
        template_values = {}
        # test = json.dumps(template_values)
        path = os.path.join(os.path.dirname(__file__), 'Like_dislike_listing.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        errors = {}
        emptyData = u''

        requestUserId = self.request.POST.get('userId')
        if requestUserId is emptyData or requestUserId is None or requestUserId.isspace():
            errors[Error_Code.missing_user_id['error']] = "UserId not provided"

        requestListingId = self.request.POST.get('listingId')
        if requestListingId is emptyData or requestListingId is None or requestListingId.isspace():
            errors[Error_Code.missing_listing_id['error']] = "ListingId not provided"

        # requestLiked = self.request.POST.get('liked')
        # if requestLiked is emptyData or requestLiked is None or requestLiked.isspace():
        #     errors[Error_Code.missing_liked['error']] = "Liked not provided"

        liked = self.request.POST.get('liked')
        if liked is emptyData or liked is None or liked.isspace():
            errors[Error_Code.missing_liked['error']] = "Liked not provided"

        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        else:

            try:
                requestUserId = int(requestUserId)
            except:
                errors[Error_Code.invalid_user_id['error']] = "UserId not valid"

            user = User.get_by_id(requestUserId)
            if user is None:
                errors[Error_Code.not_authorized['error']] = "User not authorized"

            userId = requestUserId

            try:
                requestListingId = int(requestListingId)
            except:
                errors[Error_Code.invalid_listing_id['error']] = "ListingId not valid"

            listing = Listing.get_by_id(requestListingId)
            if listing is None:
                errors[Error_Code.un_auth_listing['error']] = "Listing not authorized"

            listingId = requestListingId

            if liked != "True" and liked != "False":
                errors[Error_Code.invalid_liked['error']] = "Liked not valid"

            if liked == "True":
                liked = True
            else:
                liked = False


            if len(errors) != 0:
                error_json = json.dumps(errors)
                self.response.write(error_json)
                self.response.set_status(Error_Code.missing_invalid_parameter_error)
                return

            else:

                # make sure that the owner can't like his/her own listing
                listingOwnerId = listing.userId
                if listingOwnerId == userId:
                    errors[Error_Code.unallowed_liked['error']] = "Listing can't be liked by owner"
                    error_json = json.dumps(errors)
                    self.response.write(error_json)
                    self.response.set_status(Error_Code.missing_invalid_parameter_error)
                    return




                # check if the favorite object already exists
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
                    #TODO: do we need to make sure that the liked input is true when creating the favorite object?
                    favorite = Favorite(userId=userId, listingId=listingId, liked=liked)
                    favorite.put()
                else: # if the favorite object does exist




                    favoriteLiked = favorite.liked
                    if liked == True:
                        # user want to like the list
                        if  favoriteLiked == True:
                            # return duplicate error
                            errors[Error_Code.duplicated_liked['error']] = "The listing is already liked"
                        else:
                            # change the liked field to be true
                            favorite.liked= True
                    else:
                        # user want to unlike the list
                        if favoriteLiked == False:
                            # return error
                            errors[Error_Code.duplicated_liked['error']] = "The listing is already disliked"
                        else:
                            # change the liked field to be false
                            favorite.liked = False

                if len(errors) != 0:
                    error_json = json.dumps(errors)
                    self.response.write(error_json)
                    self.response.set_status(Error_Code.missing_invalid_parameter_error)

                else:
                    self.response.set_status(Error_Code.success)
                return

class EditListing(webapp2.RequestHandler):
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

        requestUserId = self.request.POST.get('userId')
        if requestUserId is emptyData or requestUserId is None or requestUserId.isspace():
            errors[Error_Code.missing_user_id['error']] = "UserId not provided"

        requestListingId = self.request.POST.get('listingId')
        if requestListingId is emptyData or requestListingId is None or requestListingId.isspace():
            errors[Error_Code.missing_listing_id['error']] = "ListingId not provided"


        for key, value in self.request.POST.items():
            if value is emptyData or value is None or value.isspace():
                errors[Error_Code.nothing_requested_to_change['error']] = "There was no value for key " + key
            if key != 'bedrooms' \
                and key != 'bathrooms' \
                and key != 'province' \
                and key != 'sqft' \
                and key != 'price' \
                and key != 'description' \
                and key != 'isPublished' \
                and key != 'city' \
                and key !='images' \
                and key != 'thumbnailImageIndex'\
                and key != 'address' \
                and key != 'userId' \
                and key != 'listingId':
                errors[Error_Code.unrecognized_key['error']] = "Unknown key " + key


        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        else:
            try:
                requestUserId = int(requestUserId)
            except:
                errors[Error_Code.invalid_user_id['error']] = "UserId not valid"

            user = User.get_by_id(requestUserId)
            if user is None:
                errors[Error_Code.not_authorized['error']] = "User not authorized"

            userId = requestUserId

            try:
                requestListingId = int(requestListingId)
            except:
                errors[Error_Code.invalid_listing_id['error']] = "ListingId not valid"

            listing = Listing.get_by_id(requestListingId)
            if listing is None:
                errors[Error_Code.un_auth_listing['error']] = "Listing not authorized"

            listingId = requestListingId

            if len(errors) != 0:
                error_json = json.dumps(errors)
                self.response.write(error_json)
                self.response.set_status(Error_Code.missing_invalid_parameter_error)
                return

            else:

                # make sure that the userId is the owner id of the listing
                listingOwnerId = listing.userId
                if listingOwnerId != userId:
                    errors[Error_Code.not_authorized['error']] = "Provided user ID doesn't match the owner id of the listing"
                    error_json = json.dumps(errors)
                    self.response.write(error_json)
                    self.response.set_status(Error_Code.missing_invalid_parameter_error)
                    return

                # start changing values in the listing

                for key,value in self.request.POST.items():
                    if key is not 'userId' and key is not 'listingId':
                        errors.update(listing.setProperty(key, value))

                # invalid input
                if len(errors) != 0:
                    error_json = json.dumps(errors)
                    self.response.write(error_json)
                    self.response.set_status(Error_Code.missing_invalid_parameter_error)
                    return

                self.response.set_status(Error_Code.success)
                return





# All the listings that belongs to a specific user would bound with the user email.
# (More fields in listing should be added later on.). The GET method currently get
# all the listings of the user.
class ShowListings(webapp2.RequestHandler):
    def get(self):
        #TODO: Remove testing account, should pass in user email as parameter
        user = User.query().get()
        listings = Listing.query(Listing.lister_email == user.email).fetch()
        path = os.path.join(os.path.dirname(__file__), 'Show_Listings.html')
        for listing in listings:
            template_values = {
                'lister_email': listing.lister_email,
                'bedrooms': listing.bedrooms,
                'sqft': listing.sqft,
                'bathrooms': listing.bathrooms,
                'price': listing.price,
                'description': listing.description,
                'isPublished': listing.isPublished,
                'province': listing.province,
                'city': listing.city,
                'address': listing.address,
                'images': listing.images #TODO: store image URLs from blobstore to a list
            }
            self.response.out.write(template.render(path, template_values))



