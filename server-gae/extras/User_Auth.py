import logging
from Base_Handler import *
from extras.utils import *
from extras.Error_Code import *


def user_required(handler):
    """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
    :param handler: handler to make decorator work
    :return:
    """
    def check_sign_in(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            write_error_to_response(self, {not_authorized['error']:
                                    "not authorized to change user"},
                                    not_authorized['status'])
        else:
            return handler(self, *args, **kwargs)
    return check_sign_in


class SetPasswordHandler(BaseHandler):
    """
    Sets the user password and deleted the Old token.
    It extends the BaseHandler for Basic handler utilities.
    """

    @user_required
    def post(self):
        """
        :return:
        """
        password = self.request.get('password')
        old_token = self.request.get('t')

        assert password is not None
        assert password != ''

        assert old_token is not None
        assert old_token != ''

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
    """
    Used for testing purposes on browser to check if authenticated user is
    logged in or not.
    """
    @user_required
    def get(self):
        self.render_template('../webpages/Authenticated.html')


class LogoutHandler(BaseHandler):
    """
    Handler used to unset the session and logout the session. By unset I mean
    delete the token from UserToken model.
    """
    def get(self):
        self.auth.unset_session()
        self.redirect(self.uri_for('home'))


class ForgotPasswordHandler(BaseHandler):

    def get(self):
        """
        Used to present the forgot password page by calling _serve_page
        :return:
        """
        self._serve_page()

    def post(self):
        """
        :return:
        """
        email = self.request.get('email')
        user = self.user_model.get_by_auth_id(email)
        if not user:
            logging.info('Could not find any user entry for email %s', email)
            self._serve_page(not_found=True)
            return
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        verification_url = self.uri_for('verification', type='p',
                                        user_id=user_id,signup_token=token,
                                        _full=True)

        msg = 'Send an email to user in order to reset their password. \
                  They will be able to do so by visiting <a href="{url}">{url}</a>'

        self.display_message(msg.format(url=verification_url))

    def _serve_page(self, not_found=False):
        #TODO Write specs please
        """

        :param not_found:
        :return:
        """
        username = self.request.get('username')
        params = {
            'username': username,
            'not_found': not_found
        }
        self.render_template('../webpages/Forgot.html', params)
