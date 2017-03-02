import sys
sys.path.append("../")
from google.appengine.ext import ndb
import extras.Error_Code as Error_Code
# Code from ID3

class Listing(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    bedrooms = ndb.IntegerProperty(required=True)
    sqft = ndb.IntegerProperty(required=True)
    bathrooms = ndb.FloatProperty(required=True)
    price = ndb.IntegerProperty(required=True)
    description = ndb.StringProperty(required=True)
    isPublished = ndb.BooleanProperty(required=True, default=False)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    images = ndb.BlobProperty(required=True)
    thumbnailImageIndex = ndb.IntegerProperty(required=True, default=0)
    userId = ndb.IntegerProperty(required=True)
    address = ndb.StringProperty(required=True)
    listingId = ndb.IntegerProperty(required=True,default=0)

    def set_bedrooms(self, bedrooms):
        self.bedrooms = int(bedrooms)

    def set_bathrooms(self, bathrooms):
        self.bathrooms = float(bathrooms)

    def set_price(self, price):
        self.set_price(int(price))

    def set_description(self, description):
        self.description = description

    def set_is_published(self, is_published):
        self.isPublished = is_published == 'True'

    def set_province(self, province):
        self.province = province

    def set_city(self, city):
        self.city = city

    def set_images(self, images):
        self.images = images

    def set_thumbnail_index(self, index):
        self.thumbnailImageIndex = int(index)

    def set_address(self, address):
        self.address = address

    def set_listing_id(self, listing_id):
        self.listingId = listing_id

    def set_sqft(self, sqft):
        self.sqft = float(sqft)




    def set_property(self, key, value):
        _key_to_set = {
            "price": self.set_price,
            "sqft": self.set_sqft,
            "bathrooms": self.set_bathrooms,
            "bedrooms": self.set_bedrooms,
            "description": self.set_description,
            "province": self.set_province,
            "isPublished": self.set_is_published,
            "address": self.set_address,
            "thumbnailImageIndex": self.set_thumbnail_index,
            "images": self.set_images,
            "listingId": self.set_listing_id
        }
        _key_to_set[key](value)





    def get_value_from_key(self, key):
        _key_to_get_value = {
            "price": self.price,
            "sqft": self.sqft,
            "bathrooms": self.bathrooms,
            "bedrooms": self.bedrooms,
            "description": self.description,
            "province": self.province,
            "isPublished": self.isPublished,
            "address": self.address,
            "userId": self.userId,
            "thumbnailImageIndex": self.thumbnailImageIndex,
            "images": self.images,
            "listingId": self.listingId
        }
        return _key_to_get_value[key]


