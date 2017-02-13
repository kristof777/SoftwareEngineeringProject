import logging
import json
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from BaseHandler import BaseHandler

# The implementation above renders the login page when the request
# comes via GET and processes the credentials upon POST. When authentication
# fails it renders the login page and passes the username to the template so
# that the corresponding field can be pre-filled.
class SignIn(BaseHandler):

    def get(self):
        self._serve_page()

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        d = json.loads(self.request.body)
        user_email = d['email']
        password = d['password']
        # print user_email
        # user_email = self.request.get('email')
        # password = self.request.get('password')
        try:
            u = self.auth.get_user_by_password(user_email, password, remember=True,
                                               save_session=True)
            # self.redirect(self.uri_for('home'))
            self.response.out.write("Succeed")
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s', user_email, type(e))
            self._serve_page(True)
       # listings = Listing.query(Listing.lister_email == user_email).fetch()


    def _serve_page(self, failed=False):
        user_email = self.request.get('email')
        params = {
            'user_email': user_email,
            'failed': failed
        }
        self.response.out.write("Failed")
        # self.render_template('sign_in.html', params)


