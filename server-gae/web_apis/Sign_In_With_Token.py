import logging

from extras.utils import *
from models.User import *
import sys
sys.path.append('../')
from extras.Base_Handler import BaseHandler
from extras.Error_Code import *
from API_NAME import sign_in_token_api
from extras.api_required_fields import check_required_valid


class SignInWithToken(BaseHandler):
    """
    The implementation above renders the login page when the request
    comes via GET and processes the credentials upon POST. When authentication
    fails it renders the login page and passes the username to the template so
    that the corresponding field can be pre-filled.

    @pre-condition: Post has email and password
    @post-condition: The user's token
    @return-api:
    """

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        self._serve_page()

    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(sign_in_token_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        assert values['authToken'] is not None and values['userId'] is not None

        if not(values['userId']).isdigit():
            write_error_to_response(self.response, not_authorized['error'],
                                    not_authorized['status'])
            logging.info(
                'Sign-in-with-token failed for user %s because of %s',
                values['userId'], 'invalid userId')
            return

        user = (User.get_by_auth_token(int(values['userId']), values['authToken'], subject='auth'))[0]

        assert user is not None

        self.user_model.delete_auth_token(values['userId'], values['authToken'])
        token = self.user_model.create_auth_token(values['userId'])

        assert token is not values['authToken']
        user_dict = {'authToken': token,
                     'userId': user.get_id(),
                     'email': user.email,
                     'firstName': user.first_name,
                     'lastName': user.last_name,
                     'phone1': user.phone1,
                     'phone2': user.phone2,
                     'city': user.city,
                     'province': user.province}
        self.response.out.write(json.dumps(user_dict))
        self.response.set_status(success)
