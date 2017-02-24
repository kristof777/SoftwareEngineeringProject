import json
import logging
import sys
sys.path.append("../")
import extras.Error_Code as Error_Code
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

        # For each required field, making sure it exists, is not empty
        # and also has something else other than spaces

        old_password = self.request.POST.get('password')
        if old_password is None:
            errors[Error_Code.missing_password['error']] = \
                "Old Password not provided"
        elif old_password.isspace() or old_password is empty:
            errors[Error_Code.missing_password['error']] = \
                "Old Password not provided"

        new_password = self.request.POST.get('newPassword')
        if new_password is None:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "New password not provided"
        elif new_password.isspace() or new_password is empty:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "New password not provided"

        confirmed_password = self.request.POST.get('confirmPassword')
        if confirmed_password is None:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "Confirmed password not provided"
        elif confirmed_password.isspace() or confirmed_password is empty:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "Confirmed password not provided"

        error_keys = ['email', 'firstName', 'lastName', 'password',
                     'confirmedPassword', 'phone1', 'province', 'city']
        error_values = [missing_email, missing_first_name, missing_last_name,
                        missing_password, missing_confirmed_password,
                        missing_phone_number, missing_province, missing_city]
        key_error_dict = dict(zip(error_keys, error_values))


class SetPasswordHandler(BaseHandler):

    @user_required
    def post(self):
        password = self.request.get('password')
        old_token = self.request.get('t')

        if not password or password != self.request.get('confirm_password'):
            self.display_message('passwords do not match')
            return

        user = self.user
        user.set_password(password)
        user.put()

        # remove sign up token, we don't want user to come back with an old link
        self.user_model.delete_signup_token(user.get_id(), old_token)
        self.display_message('Password updated.')


# @user_required need to be there to make sure that the user is logged in
class AuthenticatedHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('../webpages/Authenticated.html')


class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('home'))


class ForgotPasswordHandler(BaseHandler):
    def get(self):
        self._serve_page()

    def post(self):
        email = self.request.get('email')
        user = self.user_model.get_by_auth_id(email)
        if not user:
            logging.info('Could not find any user entry for email %s', email)
            self._serve_page(not_found=True)
            return
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='p', user_id=user_id,
                                        signup_token=token, _full=True)

        msg = 'Send an email to user in order to reset their password. \
                  They will be able to do so by visiting <a href="{url}">{url}</a>'

        self.display_message(msg.format(url=verification_url))

    def _serve_page(self, not_found=False):
        username = self.request.get('username')
        params = {
            'username': username,
            'not_found': not_found
        }
        self.render_template('../webpages/Forgot.html', params)
