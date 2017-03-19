import json
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
    """
    Models an individual Guest book entry with content and date.
    """
    bedrooms = ndb.IntegerProperty(required=False)
    squareFeet = ndb.IntegerProperty(required=False)
    bathrooms = ndb.FloatProperty(required=False)
    price = ndb.IntegerProperty(required=False)
    description = ndb.StringProperty(required=False)
    isPublished = ndb.BooleanProperty(required=True)
    province = ndb.StringProperty(required=False)
    city = ndb.StringProperty(required=False)
    images = ndb.BlobProperty(required=False, repeated=True)
    thumbnailImageIndex = ndb.IntegerProperty(required=False)
    userId = ndb.IntegerProperty(required=True)
    address = ndb.StringProperty(required=False)
    listingId = ndb.IntegerProperty(required=False)
    longitude = ndb.FloatProperty(required=False)
    latitude = ndb.FloatProperty(required=False)
    postalCode = ndb.StringProperty(required=False)

    """
    Assign the default values for min and max of bedrooms, bathrooms, sqFt, and price
    """
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
        """
        Resets the filter to the default max and min values
        :return: Nothing
        """
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

    def set_squareFeet(self, squareFeet):
        self.squareFeet = int(squareFeet)

    def set_longitude(self, longitude):
        self.longitude = float(longitude)

    def set_latitude(self, latitude):
        self.latitude = float(latitude)

    def set_postalCode(self, postal_code):
        self.postalCode = postal_code

    def set_property(self, key, value):
        _key_to_set = {
            "price": self.set_price,
            "squareFeet": self.set_squareFeet,
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
        assert key is not None
        assert key != ""
        _key_to_get_value = {
            "price": self.price,
            "city": self.city,
            "squareFeet": self.squareFeet,
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
        """
        Returns the desired key from the class.
        :precond key is not null
        :param key: A string representing the desired key in the class.
        :return:  The key from the class
        N.B. Python doesn't have switch cases.
        """
        assert key is not None
        assert key != ''
        return cls.get_value_from_key(cls, key)


