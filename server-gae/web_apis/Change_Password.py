import json
import logging
import sys

from extras.utils import is_invalid_password

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
        errors = {}
        empty = u''

        # For each required field, making sure it is non-null, non-empty
        # and contains more than than space characters

        old_password = self.request.POST.get('password')
        if old_password is None:
            errors[missing_password['error']] = \
                "Old Password not provided"
        elif old_password.isspace() or old_password is empty:
            errors[missing_password['error']] = \
                "Old Password not provided"

        new_password = self.request.POST.get('newPassword')
        if new_password is None:
            errors[missing_confirmed_password['error']] \
                = "New password not provided"
        elif new_password.isspace() or new_password is empty:
            errors[missing_confirmed_password['error']] \
                = "New password not provided"

        confirmed_password = self.request.POST.get('confirmPassword')
        if confirmed_password is None:
            errors[missing_confirmed_password['error']] \
                = "Confirmed password not provided"
        elif confirmed_password.isspace() or confirmed_password is empty:
            errors[missing_confirmed_password['error']] \
                = "Confirmed password not provided"

        # If there was a missing or empty field, return error
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(missing_invalid_parameter_error['status'])
            return

        if is_invalid_password(new_password):
            self.response.write(json.dumps(password_not_strong["error"]))
            self.response.set_status(password_not_strong['status'])
            return

        if new_password != confirmed_password:
            self.response.write(json.dumps(password_mismatch["error"]))
            self.response.set_status(password_mismatch['status'])
            return

        

