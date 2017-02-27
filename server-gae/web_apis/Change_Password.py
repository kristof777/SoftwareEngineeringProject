import json
import logging
import sys

from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from extras.utils import *
sys.path.append("../")
from extras.Error_Code import *
from extras.Base_Handler import BaseHandler
from models.User import *


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

        # validating if request has all required keys

        errors, values = keys_missing(error_keys, self.request.POST)
        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            print (errors)
            write_error_to_response(self.response, errors,
                                    missing_invalid_parameter_error)
            return


        #attempt to get the current user by the old password. Will throw an
        # exception if the password or e-mail are unrecognized.
        try:
            user = User.get_by_id(int(values["userId"]))
            user_dict = self.auth.get_user_by_password(
                user.email, values['oldPassword'], remember=True,
                save_session=True)

        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s',
                         values['userId'], type(e))
            write_error_to_response(self.response, not_authorized["error"],
                                    not_authorized['status'])
            return

        if not is_valid_password(values['newPassword']):
            write_error_to_response(self.response, password_not_strong['error'],
                         password_not_strong['status'])
            return

        if values['newPassword'] != values['confirmedPassword']:
            write_error_to_response(self.response, password_mismatch["error"],
                         password_mismatch['status'])
            return


        print type(user)

        try:
            User.set_password(user, values['newPassword'])
            user_dict = self.auth.get_user_by_password(
                user.email, values['newPassword'], remember=True,
                save_session=True)
        except:
            assert(False)


        #self.auth.store.delete_auth_token(user['userId'], user['token'])
        user_dict = {'token': user_dict['token']}
        self.response.write(json.dumps(user_dict))
        self.response.set_status(200)
        return
