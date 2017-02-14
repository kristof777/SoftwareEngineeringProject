import logging
import json
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from BaseHandler import BaseHandler


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
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        print self.request.POST
        user_email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        try:
            u = self.auth.get_user_by_password(user_email, password,
                                               remember=True, save_session=True)
            self.response.out.write("Succeed")
        except (InvalidAuthIdError, InvalidPasswordError) as e:
            logging.info('Sign-in failed for user %s because of %s',
                         user_email, type(e))
            d = json.dumps('{errorKey: error}')
            self.response.write(d)
            self.response.set_status(401)

    def _serve_page(self, failed=False):
        user_email = self.request.get('email')
        params = {
            'user_email': user_email,
            'failed': failed
        }
        self.response.write("Failed")
        self.render_template('sign_in.html', params)


