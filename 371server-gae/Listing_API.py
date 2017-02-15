import os
import logging
import webapp2
from google.appengine.ext.webapp import template
from models.listing import Listing
from models.user import User
import json
import main
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
        try:
            user = User.get_by_id(requestUserId)
            userId = requestUserId
        except (KeyError) as e:
            errors['api.error.invalid_user'] = "Can't find user"
        try:
            bedrooms = int(self.request.POST.get('bedrooms'))
        except (KeyError) as e:
            errors['api.error.missing_bedroom'] = "Number of bedrooms not provided"
        try:
            sqft = int(self.request.POST.get('sqft'))
        except (KeyError) as e:
            errors['api.error.missing_sqft'] = "Square feet not provided"
        try:
            bathrooms = int(self.request.POST.get('bathrooms'))
        except (KeyError) as e:
            errors['api.error.missing_bathroom'] = "Number of bathrooms not provided"
        try:
            price = int(self.request.POST.get('price'))
        except (KeyError) as e:
            errors['api.error.missing_price'] = "Price not provided"
        try:
            description = self.request.POST.get('description')
        except (KeyError) as e:
            errors['api.error.missing_description'] = "Description not provided"
        try:
            isPublished = self.request.POST.get('isPublished') != ''
        except (KeyError) as e:
            errors['api.error.invalid_publication'] = "Invalid Publication"
        try:
            province = self.request.POST.get('province')
        except (KeyError) as e:
            errors['api.error.invalid_province'] = "Province not valid"
        try:
            city = self.request.POST.get('city')
        except (KeyError) as e:
            errors['api.error.invalid_city'] = "City not valid"
        try:
            address = self.request.POST.get('address')
        except (KeyError) as e:
            errors['api.error.invalid_address'] = "Address not valid"
        try:
            images = self.request.POST.get('images')
        except (KeyError) as e:
            errors['api.error.missing_image'] = "There should be at least one image present"


        try:
            listing = Listing(userId= userId, bedrooms=bedrooms, sqft=sqft, bathrooms=bathrooms,
                             price=price, description=description, isPublished=isPublished, province=province,
                             city=city, address=address, images=images)
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
