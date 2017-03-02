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


    def set_property(self, key, value):
        if key == 'bedrooms':
            self.bedrooms = int(value)
            return
        if key == 'sqft':
            self.sqft = int(value)
            return
        if key == 'bathrooms':
            self.bathrooms = float(value)
            return
        if key == 'price':
            self.price = int(value)
            return
        if key == 'description':
            self.description = value
            return
        if key == 'isPublished':
            if value == 'False':
                self.isPublished = False
            else:
                self.isPublished = True
            return
        if key == 'province':
            self.province = value
            return
        if key == 'city':
            self.city = value
            return
        if key == 'images':
            self.images = value
            return
        if key == 'thumbnailImageIndex':
            self.thumbnailImageIndex = int(value)
            return
        if key == 'address':
            self.address = value
            return
        if key == 'listingId':
            self.listingId = int(value)
        return


    def get_value_from_key(self, key):
        _key_to_get_value = {
            "price": self.price,
            "city": self.city,
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

    @classmethod
    def get_key(cls, key):
        if key == 'bedrooms':
            return cls.bedrooms
        if key == 'sqft':
            return cls.sqft
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


