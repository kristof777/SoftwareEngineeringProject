import time
import webapp2_extras
from google.appengine.ext import ndb
from webapp2_extras import security
from webapp2_extras.appengine.auth.models import User as Webapp2User

class User(Webapp2User):

    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    phone1 = ndb.StringProperty(required=True)
    phone2 = ndb.StringProperty(required=False)
    province = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    postal_code = ndb.StringProperty(required=True)


    def set_password(self, raw_password):
        """Sets the password for the current user

        :param raw_password:
            The raw password which will be hashed and stored
        """
        self.password = security.generate_password_hash(raw_password)



    # @classmethod
    # def build_key(cls, email):
    #     return ndb.Key(cls, email)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token

        :param user_id:
            The user_id of the requesting user
        :param token:
            The token string to be verified
        :returns
            A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
        """

        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None
