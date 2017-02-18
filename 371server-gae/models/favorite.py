from google.appengine.ext import ndb


class Favorite(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    listingId = ndb.IntegerProperty(required=True)
    userId = ndb.IntegerProperty(required=True)
    liked = ndb.BooleanProperty(required=True, default=True)
