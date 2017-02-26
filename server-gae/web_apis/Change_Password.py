import json
import logging
import sys

from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from extras.utils import *
from models import User

sys.path.append("../")
from extras.Error_Code import *
from extras.Base_Handler import BaseHandler


# We need to decide whether uses are allowed to
# access certain resources depending on if they are logged in or not.
def user_required(handler):
    """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
    """
    def check_sign_in(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('signin'), abort=True)
        else:
            return handler(self, *args, **kwargs)
    return check_sign_in


class ChangePassword(BaseHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be old_password,
                   new_password, and confirmed_password. If any of these is not
                   present an appropriate error and status code 40 is returned.

                   new_password and confirmed_password are expected to be equal
                   then if not then appropriate missing_invalid_parameter_error
                   is returned.

                   new passwords must be 8 in length, and have at least one
                   uppercase, lowercase, and numeric character or it will return
                   a missing_invalid_parameter_error.

        @post-cond: A users password is changed in the database. Token and userId is returned as an response
                    object.
    """
    def get(self):
        self.render_template('../webpages/Change_Password.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        # For each required field, making sure it is non-null, non-empty
        # and contains more than than space characters

        error_keys = ['oldPassword', 'newPassword', 'confirmedPassword', 'userId']
        error_values = [missing_password, missing_new_password, missing_new_password_confirmed, missing_user_id]
        key_error_dict = dict(zip(error_keys, error_values))

        # validating if request has all required keys
        errors, values = keys_validation(key_error_dict, self.request.POST)
        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            print errors
            return_error(self, errors, missing_invalid_parameter_error)
            return

        #attempt to get the current user by the old password. Will throw an
        # exception if the password or e-mail are unrecognized.
        try:
            User.get_by_id(int(values["userId"]))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            print type(e)
            print values['userId']
            print values['oldPassword']
            logging.info('Sign-in failed for user %s because of %s',
                         values['userId'], type(e))
            return_error(self, not_authorized["error"], not_authorized['status'])
            return

        if is_invalid_password(values['newPassword']):
            return_error(self, password_not_strong['error'],
                         password_not_strong['status'])
            return

        if values['newPassword'] != values['confirmedPassword']:
            return_error(self, password_mismatch["error"],
                         password_mismatch['status'])
            return

        user = self.auth.get_user_by_session()
        user.set_password(values['newPassword'])

        self.auth.set_session(user, token=None, token_ts=None, cache_ts=None,
                    remember=True)

        user = self.auth.get_user_by_session(session=True)

        self.response.write(json.dumps(user['token']))
        self.response.set_status(200)
        return
