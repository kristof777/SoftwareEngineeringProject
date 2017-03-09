import sys
from google.appengine.ext import ndb
sys.path.append("../")


class Listing(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    bedrooms = ndb.IntegerProperty(required=True)
    squarefeet = ndb.IntegerProperty(required=True)
    bathrooms = ndb.FloatProperty(required=True)
    price = ndb.IntegerProperty(required=True)
    description = ndb.StringProperty(required=True)
    isPublished = ndb.BooleanProperty(required=True, default=False)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    images = ndb.BlobProperty(repeated=True)
    thumbnailImageIndex = ndb.IntegerProperty(required=True, default=0)
    userId = ndb.IntegerProperty(required=True)
    address = ndb.StringProperty(required=True)
    listingId = ndb.IntegerProperty(required=True,default=0)
    longitude = ndb.FloatProperty(required=True, default=0)
    latitude = ndb.FloatProperty(required=True, default=0)

    def set_bedrooms(self, bedrooms):
        self.bedrooms = int(bedrooms)

    def set_bathrooms(self, bathrooms):
        self.bathrooms = float(bathrooms)

    def set_price(self, price):
        self.price = int(price)

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

    def set_squarefeet(self, squarefeet):
        self.squarefeet = int(squarefeet)

    def set_longitude(self, longitude):
        self.longitude = float(longitude)

    def set_latitude(self, latitude):
        self.latitude = float(latitude)

    def set_property(self, key, value):
        _key_to_set = {
            "price": self.set_price,
            "squarefeet": self.set_squarefeet,
            "bathrooms": self.set_bathrooms,
            "bedrooms": self.set_bedrooms,
            "description": self.set_description,
            "province": self.set_province,
            "isPublished": self.set_is_published,
            "address": self.set_address,
            "thumbnailImageIndex": self.set_thumbnail_index,
            "images": self.set_images,
            "listingId": self.set_listing_id,
            "city": self.set_city,
            "longitude": self.longitude,
            "latitude": self.latitude
        }
        _key_to_set[key](value)

    def get_value_from_key(self, key):
        _key_to_get_value = {
            "price": self.price,
            "city": self.city,
            "squarefeet": self.squarefeet,
            "bathrooms": self.bathrooms,
            "bedrooms": self.bedrooms,
            "description": self.description,
            "province": self.province,
            "isPublished": self.isPublished,
            "address": self.address,
            "userId": self.userId,
            "thumbnailImageIndex": self.thumbnailImageIndex,
            "images": self.images,
            "listingId": self.listingId,
            "longitude": self.longitude,
            "latitude": self.latitude
        }
        return _key_to_get_value[key]

    @classmethod
    def get_key(cls, key):
        if key == 'bedrooms':
            return cls.bedrooms
        if key == 'squarefeet':
            return cls.squarefeet
        if key == 'bathrooms':
            return cls.bathrooms
        if key == 'price':
            return cls.price
        if key == 'description':
            return cls.description
        if key == 'isPublished':
            return cls.isPublished
        if key == 'province':
            return cls.province
        if key == 'city':
            return cls.city
        if key == 'images':
            return cls.images
        if key == 'thumbnailImageIndex':
            return cls.thumbnailImageIndex
        if key == 'address':
            return cls.address
        if key == 'listingId':
            return cls.listingId
        if key == 'longitude':
            return cls.longitude
        if key == 'latitude':
            return cls.latitude


