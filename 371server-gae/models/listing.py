from google.appengine.ext import ndb


class Listing(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    lister_email = ndb.StringProperty(required=True)
    bedrooms = ndb.StringProperty(required=True)
    sqft = ndb.StringProperty(required=True)
    bathrooms = ndb.StringProperty(required=True)
    price = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    isPublished = ndb.BooleanProperty(required=True, default=False)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    images = ndb.BlobProperty()

    @classmethod
    def build_key(cls, lister_email, bedrooms, sqft, bathrooms, price, description, province, city):
        return ndb.Key(cls, lister_email+bedrooms+sqft+bathrooms+price+description+province+city)
