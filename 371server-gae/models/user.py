from google.appengine.ext import ndb


class User(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    phone1 = ndb.StringProperty(required=True)
    phone2 = ndb.StringProperty(required=True)
    phone3 = ndb.StringProperty(required=True)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)

    @classmethod
    def build_key(cls, email):
        return ndb.Key(cls, email)
