import os
import logging
import webapp2
from google.appengine.ext.webapp import template
from models.listing import Listing
from models.user import User
import json
import main
import error_code
import unittest

# The GET method is simply get the html page ( in the browser for back-end testing)
# for user inputs. The POST method is similar to create_user, what it does is to get
# all the information from what the user typed, and generate a new listing that belongs
# to the current user (with email as the key).
class CreateListing(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'

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
        errors = {}
        requestUserId = int(self.request.POST.get('userId'))
        if requestUserId is None:
            errors[error_code.missing_user_id['error']] = "UserId not provided"

        user = User.get_by_id(requestUserId)
        if user is None:
            errors[error_code.un_auth_listing['error']] = "listing unauthorized"

        userId = requestUserId
        bedrooms = int(self.request.POST.get('bedrooms'))
        if bedrooms is None:
            errors[error_code.missing_bedrooms['error']] = "Number of bedrooms not provided"
        sqft = int(self.request.POST.get('sqft'))
        if sqft is None:
            errors[error_code.missing_sqft['error']] = "Square feet not provided"
        bathrooms = int(self.request.POST.get('bathrooms'))
        if bathrooms is None:
            errors[error_code.missing_bathrooms['error']] = "Number of bathrooms not provided"
        price = int(self.request.POST.get('price'))
        if price is None:
            errors[error_code.missing_price['error']] = "Price not provided"
        description = self.request.POST.get('description')
        if description is None:
            error_code[error_code.missing_description['error']] = "Description not provided"
        isPublished = self.request.POST.get('isPublished') != ''
        province = self.request.POST.get('province')
        if province is None:
            errors[error_code.missing_province['error']] = "Province not provided"
        city = self.request.POST.get('city')
        if city is None:
            errors[error_code.missing_city['error']] = "City not provided"
        address = self.request.POST.get('address')
        if address is None:
            errors[error_code.missing_address['error']] = "Address not provided"
        images = self.request.POST.get('images')
        if images is None:
            errors[error_code.missing_image['error']] = "Images not provided"
        thumbnailImageIndex = self.request.POST.get('thumbnailImageIndex')
        if thumbnailImageIndex is None:
            errors[error_code.missing_image_index['error']] = "thumbnail not provided"


        try:
            listing = Listing(userId= userId, bedrooms=bedrooms, sqft=sqft, bathrooms=bathrooms,
                             price=price, description=description, isPublished=isPublished, province=province,
                             city=city, address=address, images=images, thumbnailImageIndex=thumbnailImageIndex)
            listing.put()
            listing.listingId = listing.key.id()
            self.response.out.write(listing.listingId)
        except RuntimeError as e:
            logging.info('Creating failed for user %s because of %s', userId, type(e))
            d = json.dumps('{errorKey: error}')
            self.response.write(d)
            self.response.set_status(401)

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





class TestListingAPIHandlers(unittest.TestCase):
   def test_create_listing(self):
       # Build a request object passing the URI path to be tested.
       # You can also pass headers, query arguments etc.
       request = webapp2.Request.blank('/createlisting')
       # Get a response for that request.
       response = request.get_response(main.app)

       # Let's check if the response is correct.
       self.assertEqual(response.status_int, 200)
