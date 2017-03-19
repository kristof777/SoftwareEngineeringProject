from google.appengine.api import mail
from extras.Base_Handler import BaseHandler
from extras.Utils import *
from models.FB import FBLogin
from models.Favorite import Favorite
from models.Listing import Listing
from models.Message import Message
from models.User import User
from webapp2_extras.appengine.auth.models import UserToken, Unique
from extras.Test_Databse import *
import Main


class InitializeDB(BaseHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be email, firstName, lastName,
                   password, confirmedPassword, phone1, phone2(optional),
                   city, postalCode. If any of these is not present an
                   appropriate error and status code 400 is returned.

                   password and ConfirmedPassword are expected to be equal then
                   if not then appropriate missing_invalid_parameter_error is
                   returned.

                   If email already exists, then an error is returned.
        @post-cond: An user with provided information is created in the
                    database. Token and userId is returned as an response
                    object.
    """

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        pass

    def post(self):
        models_list = [FBLogin, Favorite, Listing, Message, User, UserToken,
                       Unique]

        for model in models_list:
            for member in model.query().fetch():
                print("deleting" + str(member))
                member.key.delete()
        responses = []
        for user in users:
            response, _ = get_response_from_post(Main, user, 'createUser')
            responses.append(response)

        number_of_responses = len(responses)
        for i in range(len(listings_published)):
            listing = listings_published[i]
            listing["userId"] = responses[i % number_of_responses]["userId"]
            listing["authToken"] = responses[i % number_of_responses][
                "authToken"]
            get_response_from_post(Main, listing, 'createListing')

        for i in range(len(listing_unpublished)):
            listing = listing_unpublished[i]
            listing["userId"] = responses[i % number_of_responses]["userId"]
            listing["authToken"] = responses[i % number_of_responses][
                "authToken"]
            get_response_from_post(Main, listing, 'createListing')

        create_dummy_listings_for_testing(Main, random_listings, random_users)
        write_success_to_response(self.response, {})
