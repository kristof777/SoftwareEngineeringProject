import sys
from google.appengine.ext import ndb
sys.path.append("../")

DEFAULT_BEDROOMS_MAX = 10
DEFAULT_BEDROOMS_MIN = 1
DEFAULT_BATHROOMS_MAX = 10.0
DEFAULT_BATHROOMS_MIN = 1.0
DEFAULT_SQFT_MAX = 10000
DEFAULT_SQFT_MIN = 0
DEFAULT_PRICE_MAX = 999999999
DEFAULT_PRICE_MIN = 10


class Listing(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    bedrooms = ndb.IntegerProperty(required=False)
    squarefeet = ndb.IntegerProperty(required=False)
    bathrooms = ndb.FloatProperty(required=False)
    price = ndb.IntegerProperty(required=False)
    description = ndb.StringProperty(required=False)
    isPublished = ndb.BooleanProperty(required=False, default=False)
    province = ndb.StringProperty(required=False)
    city = ndb.StringProperty(required=False)
    images = ndb.BlobProperty(repeated=True)
    thumbnailImageIndex = ndb.IntegerProperty(required=False, default=0)
    userId = ndb.IntegerProperty(required=False)
    address = ndb.StringProperty(required=False)
    listingId = ndb.IntegerProperty(required=False,default=0)
    longitude = ndb.FloatProperty(required=False, default=0)
    latitude = ndb.FloatProperty(required=False, default=0)
    postalCode = ndb.StringProperty(required=False)

    numeric_filter_bounds = {
        "bedrooms_min": DEFAULT_BEDROOMS_MIN,
        "bedrooms_max": DEFAULT_BEDROOMS_MAX,
        "bathrooms_min": DEFAULT_BATHROOMS_MIN,
        "bathrooms_max": DEFAULT_BATHROOMS_MAX,
        "sqft_min": DEFAULT_SQFT_MIN,
        "sqft_max": DEFAULT_SQFT_MAX,
        "price_min": DEFAULT_PRICE_MIN,
        "price_max": DEFAULT_PRICE_MAX
    }

    @classmethod
    def reset_filter(cls):
        cls.numeric_filter_bounds['bedrooms_min'] = DEFAULT_BEDROOMS_MIN
        cls.numeric_filter_bounds['bedrooms_max'] = DEFAULT_BEDROOMS_MAX
        cls.numeric_filter_bounds['bathrooms_min'] = DEFAULT_BATHROOMS_MIN
        cls.numeric_filter_bounds['bathrooms_max'] = DEFAULT_BATHROOMS_MAX
        cls.numeric_filter_bounds['sqft_min'] = DEFAULT_SQFT_MIN
        cls.numeric_filter_bounds['sqft_max'] = DEFAULT_SQFT_MAX
        cls.numeric_filter_bounds['price_min'] = DEFAULT_PRICE_MIN
        cls.numeric_filter_bounds['price_max'] = DEFAULT_PRICE_MAX

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

    def set_postalCode(self, postal_code):
        self.postalCode = postal_code

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
            "longitude": self.set_longitude,
            "latitude": self.set_latitude,
            "postalCode": self.set_postalCode
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
            "latitude": self.latitude,
            "postalCode": self.latitude
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
        if key == 'postalCode':
            return cls.postalCode


