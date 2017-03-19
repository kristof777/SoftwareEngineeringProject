# when websites send us an activation link after a registration,
# the url usually contain their equivalent of signup tokens.
import logging
from extras.Base_Handler import BaseHandler


class VerificationHandler(BaseHandler):
    """
    Class used to handle get and post.
    Get:
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

        @return: A dictionary with all the user details attached with token,
         and userId is sent on valid request. is used to render an HTML page.

    Post: Doesn't exist
    """
    def get(self, *args, **kwargs):
        user = None
        user_id = kwargs['user_id']
        signup_token = kwargs['signup_token']
        verification_type = kwargs['type']
        user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token,
                                                     'signup')
        if not user:
            logging.info(
                'Could not find any user with id "%s" signup token "%s"',
                user_id, signup_token)
            self.abort(404)

        # store user data in the session
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

        if verification_type == 'v':  # remove signup token, we don't want users
            # to come back with an old link
            self.user_model.delete_signup_token(user.get_id(), signup_token)

        if not user.verified:
            user.verified = True
            user.put()
            # self.display_message('User email address has been verified.')
            return
        elif verification_type == 'p':
            # supply user to the page
            params = {
                'user': user,
                'token': signup_token
            }
            self.render_template('Reset_Password.html', params)
        else:
            logging.info('verification type not supported.')
            self.abort(404)
