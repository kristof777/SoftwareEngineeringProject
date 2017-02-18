from google.appengine.ext import ndb


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
    images = ndb.BlobProperty()
    thumbnailImageIndex = ndb.IntegerProperty()
    userId = ndb.IntegerProperty()
    address = ndb.StringProperty()

    @classmethod
    def build_key(cls, lister_email, bedrooms, sqft, bathrooms, price, description, province, city):
        return ndb.Key(cls, lister_email+str(bedrooms)+str(sqft)+str(bathrooms)+str(price)+description+province+city)
