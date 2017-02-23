import sys
sys.path.append("../")
from google.appengine.ext import ndb
import extras.Error_Code as Error_Code
# Code from ID3

class Listing(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    bedrooms = ndb.IntegerProperty(required=True)
    sqft = ndb.IntegerProperty(required=True)
    bathrooms = ndb.IntegerProperty(required=True)
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


    def setProperty(self, key, value):
        errors = {}
        if key == 'bedrooms':
            try:
                self.bedrooms = int(value)
            except:
                errors[Error_Code.invalid_bedrooms['error']] = "Number of bedrooms not valid"
            return errors
        if key == 'sqft':
            try:
                self.sqft = int(value)
            except:
                errors[Error_Code.invalid_sqft['error']] = "Square feet not valid"
            return errors
        if key == 'bathrooms':
            try:
                self.bathrooms = int(value)
            except:
                errors[Error_Code.invalid_bathrooms['error']] = "Number of bathrooms not valid"
            return errors
        if key == 'price':
            try:
                self.price = int(value)
            except:
                errors[Error_Code.invalid_price['error']] = "Price not valid"
            return errors
        if key == 'description':
            self.description = value
            return errors
        if key == 'isPublished':
            if value == 'False':
                self.isPublished = False
            elif value == 'True':
                self.isPublished = True
            else:
                errors[Error_Code.invalid_published['error']] = "isPublished not valid"
            return errors
        if key == 'province':
            self.province = value
            return errors
        if key == 'city':
            self.city = value
            return errors
        if key == 'images':
            self.images = value
            return errors
        if key == 'thumbnailImageIndex':
            try:
                self.thumbnailImageIndex = int(value)
            except:
                errors[Error_Code.invalid_thumbnail_image_index['error']] = "Thumbnail image index not valid"
            return errors
        if key == 'address':
            self.address = value
            return errors
        if key == 'listingId':
            try:
                self.listingId = int(value)
            except:
                errors[Error_Code.invalid_listing_id['error']] = "listingId not valid"
        return errors

