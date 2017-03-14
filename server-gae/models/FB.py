import datetime
from google.appengine.ext import ndb


class FBLogin(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    fb_id = ndb.IntegerProperty(required=True, default = 0)
    user_id = ndb.IntegerProperty(required=True)
    created_date = ndb.DateProperty(required=True,
                                   default=datetime.datetime.now())

