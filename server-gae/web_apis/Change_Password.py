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
        @pre-cond: Expecting keys to be currentPassword,
                   password, and confirmedPassword. If any of these is not
                   present an appropriate error and status code 40 is returned.

                   password and ConfirmedPassword are expected to be equal then
                   if not then appropriate missing_invalid_parameter_error is
                   returned.

                   password must be 8 in length, and have at least one upercase,
                   lowercase, and numeric character or it will return a
                   missing_invalid_parameter_error.

        @post-cond: An user with provided information is created in the
                    database. Token and userId is returned as an response
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

        password = self.request.POST.get('password')
        if password is None:
            errors[Error_Code.missing_password['error']] = \
                "Password not provided"
        elif password.isspace() or password is empty:
            errors[Error_Code.missing_password['error']] = \
                "Password not provided"

        confirmed_password = self.request.POST.get('newPassword')
        if confirmed_password is None:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "New password not provided"
        elif confirmed_password.isspace() or confirmed_password is empty:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "New password not provided"

        confirmed_password = self.request.POST.get('confirmPassword')
        if confirmed_password is None:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "Confirmed password not provided"
        elif confirmed_password.isspace() or confirmed_password is empty:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "Confirmed password not provided"


# when websites send us an activation link after a registration,
# the url usually contain their equivalent of signup tokens.
class VerificationHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = None
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']

        user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token, 'signup')

        if not user:
            logging.info('Could not find any user with id "%s" signup token "%s"',
                         user_id, signup_token)
            self.abort(404)

        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        if verification_type == 'v': #remove signup token, we don't want users to come back with an old link
         self.user_model.delete_signup_token(user.get_id(), signup_token)

        if not user.verified:
            user.verified = True
            user.put()

            self.display_message('User email address has been verified.')
            return
        elif verification_type == 'p':
            # supply user to the page
            params = {
                'user': user,
                'token': signup_token
            }
            self.render_template('../webpages/Reset_Password.html', params)
        else:
            logging.info('verification type not supported.')
            self.abort(404)


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
