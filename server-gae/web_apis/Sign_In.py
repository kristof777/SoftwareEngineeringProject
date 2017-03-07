import logging

from extras.utils import *
import sys
sys.path.append('../')
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from extras.Base_Handler import BaseHandler
from extras.Error_Code import *


class SignIn(BaseHandler):
    """
    The implementation above renders the login page when the request
    comes via GET and processes the credentials upon POST. When authentication
    fails it renders the login page and passes the username to the template so
    that the corresponding field can be pre-filled.

    @pre-condition: Post has email and password
    @post-condition:
    @return-api:
    """

    def get(self):
        self._serve_page()

    def post(self):

        # validating if request has all required keys
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        error_keys = ['email', 'password']

        errors, values = keys_missing(error_keys, self.request.POST)
        message = {}
        user_email = self.request.POST.get('email')

        # checking for empty fields
        if user_email is None:
            message[missing_email['error']] = 'Missing user email'
        password = self.request.POST.get('password')
        if password is None:
            message[missing_password['error']] = 'Missing password'

        if len(message.keys()) > 0:
            write_error_to_response(self.response, message,
                                    missing_invalid_parameter)
            return

        assert user_email is not None and password is not None
        try:
            # sign in and return user information.
            user = self.auth.get_user_by_password(
                user_email.lower(), password, remember=True, save_session=True)

            user_dict = {'token': user['token'],
                         'userId': user['user_id'],
                         'email': user['email'],
                         'firstName': user['first_name'],
                         'lastName': user['last_name'],
                         'phone1': user['phone1'],
                         'phone2': user['phone2'],
                         'city': user['city'],
                         'province': user['province']}
            write_success_to_response(self.response,user_dict)

        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s',
                         user_email, type(e))
            write_error_to_response(self.response, not_authorized['error'],
                                    not_authorized['status'])

    def _serve_page(self, failed=False):
        user_email = self.request.get('email')
        params = {
            'user_email': user_email,
            'failed': failed
        }
        self.response.write('Failed')
        self.render_template('../webpages/Sign_In.html', params)
