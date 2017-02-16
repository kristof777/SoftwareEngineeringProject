import os
import webapp2
from google.appengine.ext.webapp import template
from models.listing import Listing
from models.user import User
import json
import error_code

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
        path = os.path.join(os.path.dirname(__file__), 'create_listing.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        emptyData = u''
        errors = {}

        # check if there's any missing field, if so, just return to the user what all is missing
        # if not, then go ahead and check validity
        requestUserId = self.request.POST.get('userId')
        if requestUserId is emptyData or requestUserId is None or requestUserId.isspace():
            errors[error_code.missing_user_id['error']] = "UserId not provided"

        bedrooms = self.request.POST.get('bedrooms')
        if bedrooms is emptyData or bedrooms is None or bedrooms.isspace():
            errors[error_code.missing_bedrooms['error']] = "Number of bedrooms not provided"

        sqft = self.request.POST.get('sqft')
        if sqft is emptyData or sqft is None or sqft.isspace():
            errors[error_code.missing_sqft['error']] = "Square feet not provided"

        bathrooms = self.request.POST.get('bathrooms')
        if bathrooms is emptyData or bathrooms is None or bathrooms.isspace():
            errors[error_code.missing_bathrooms['error']] = "Number of bathrooms not provided"

        price = self.request.POST.get('price')
        if price is emptyData or price is None or price.isspace():
            errors[error_code.missing_price['error']] = "Price not provided"

        description = self.request.POST.get('description')
        if description is emptyData or description is None or description.isspace():
            errors[error_code.missing_description['error']] = "Description not provided"

        isPublished = self.request.POST.get('isPublished') != ''

        province = self.request.POST.get('province')
        if province is emptyData or province is None or province.isspace():
            errors[error_code.missing_province['error']] = "Province not provided"

        city = self.request.POST.get('city')
        if city is emptyData or city is None or city.isspace():
            errors[error_code.missing_city['error']] = "City not provided"

        address = self.request.POST.get('address')
        if address is emptyData or address is None or address.isspace():
            errors[error_code.missing_address['error']] = "Address not provided"

        images = str(self.request.POST.get('images'))
        if images is '' or images == 'None' or images.isspace():
            errors[error_code.missing_image['error']] = "Images not provided"

        thumbnailImageIndex = self.request.POST.get('thumbnailImageIndex')
        if thumbnailImageIndex is emptyData or thumbnailImageIndex is None or thumbnailImageIndex.isspace():
            errors[error_code.missing_image_index['error']] = "thumbnail not provided"

        # if there are missing fields, return
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(
                error_code.missing_invalid_parameter_error)
            return

        else:  # check validity for integer fields (userId, bedrooms, bathrooms, sqft, price, thumbnailImageIndex)

            try:
                requestUserId = int(requestUserId)
            except:
                errors[error_code.invalid_user_id['error']] = "UserId not valid"

            # find the correct user with userId
            user = User.get_by_id(requestUserId)
            if user is None:
                errors[error_code.un_auth_listing['error']] = "listing unauthorized"

            userId = requestUserId

            try:
                bedrooms = int(bedrooms)
            except:
                errors[error_code.invalid_bedrooms['error']] = "Number of bedrooms not valid"

            try:
                 sqft = int(sqft)
            except:
                errors[error_code.invalid_sqft['error']] = "Square feet not valid"

            try:
                bathrooms = int(bathrooms)
            except:
                errors[error_code.invalid_bathrooms['error']] = "Number of bathrooms not valid"

            try:
                price = int(self.request.POST.get('price'))
            except:
                errors[error_code.invalid_price['error']] = "Price not valid"


            try:
                thumbnailImageIndex = int(thumbnailImageIndex)
            except:
                errors[error_code.invalid_thumbnail_image_index['error']] = "Thumbnail image index not valid"


            if len(errors) != 0:    # if there is invalid fields
                error_json = json.dumps(errors)
                self.response.write(error_json)
                self.response.set_status(
                    error_code.missing_invalid_parameter_error)
                return
            else:
                # all set
                listing = Listing(userId=userId, bedrooms=bedrooms, sqft=sqft, bathrooms=bathrooms,
                                  price=price, description=description, isPublished=isPublished, province=province,
                                  city=city, address=address, images=images, thumbnailImageIndex=thumbnailImageIndex)
                listing.put()
                listing.listingId = listing.key.id()
                self.response.write(json.dumps({"listingId": listing.listingId}))
                self.response.set_status(error_code.success)


# All the listings that belongs to a specific user would bound with the user email.
# (More fields in listing should be added later on.). The GET method currently get
# all the listings of the user.
class ShowListings(webapp2.RequestHandler):
    def get(self):
        #TODO: Remove testing account, should pass in user email as parameter
        user = User.query().get()
        listings = Listing.query(Listing.lister_email == user.email).fetch()
        path = os.path.join(os.path.dirname(__file__), 'show_listings.html')
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



