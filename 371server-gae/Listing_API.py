import os
import webapp2
from google.appengine.ext.webapp import template
from models.listing import Listing
from models.user import User

# The GET method is simply get the html page ( in the browser for back-end testing)
# for user inputs. The POST method is similar to create_user, what it does is to get
# all the information from what the user typed, and generate a new listing that belongs
# to the current user (with email as the key).
class CreateListing(webapp2.RequestHandler):
    def get(self):
        template_values = {
            # 'first_name': user2.first_name,
            # 'last_name': user2.last_name
        }
        # test = json.dumps(template_values)
        path = os.path.join(os.path.dirname(__file__), 'create_listing.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):

       #TODO: Remove testing account
        user = User.query().get()
        lister_email = user.email_address
        bedrooms = int(self.request.get('bedrooms'))
        sqft = int(self.request.get('sqft'))
        bathrooms = int(self.request.get('bathrooms'))
        price = int(self.request.get('price'))
        description = self.request.get('description')
        isPublished = self.request.get('isPublished') != ''
        province = self.request.get('province')
        city = self.request.get('city')
        images = self.request.get('images')

        listing = Listing(lister_email=lister_email, bedrooms=bedrooms, sqft=sqft, bathrooms=bathrooms,
                          price=price, description=description, isPublished=isPublished, province=province,
                          city=city, images=images)
        key = Listing.build_key(lister_email, bedrooms, sqft, bathrooms, price, description, province, city)
        listing.key = key
        listing.put()

        self.response.out.write('<h1>New listing created!</h1>')

# All the listings that belongs to a specific user would bound with the user email.
# (More fields in listing should be added later on.). The GET method currently get
# all the listings of the user.
class ShowListings(webapp2.RequestHandler):
    def get(self):
        #TODO: Remove testing account, should pass in user email as parameter
        user = User.query().get()
        listings = Listing.query(Listing.lister_email == user.email_address).fetch()
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
                'images': listing.images #TODO: store image URLs from blobstore to a list
            }
            self.response.out.write(template.render(path, template_values))

