# when websites send us an activation link after a registration,
# the url usually contain their equivalent of signup tokens.
import logging
from extras.Base_Handler import BaseHandler


class VerificationHandler(BaseHandler):
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
