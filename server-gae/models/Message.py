import datetime
from google.appengine.ext import ndb


class Message(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    listingId = ndb.IntegerProperty(required=True)
    senderId = ndb.IntegerProperty(required=True)
    message = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    received = ndb.BooleanProperty(required=True, default=False)
    createdDate = ndb.DateProperty(required=True, default=datetime.datetime.now())
