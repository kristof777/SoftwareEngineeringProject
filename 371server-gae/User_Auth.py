from BaseHandler import *
import logging
import json

#
# We need to decide whether uses are allowed to
# access certain resources depending on if they are logged in or not.
def user_required(handler):
    """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
    """
    def check_signin(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            self.redirect(self.uri_for('signin'), abort=True)
        else:
            return handler(self, *args, **kwargs)
    return check_signin


class CreateUser(BaseHandler):
    def get(self):
        self.render_template('create_user.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        errros = {}
        userInfoProvided = json.loads(self.request.body)
        try:
            email = userInfoProvided['email']
        except (KeyError) as e:
            errros['api.error.missing_email'] = "Email not provided"
        try:
            firstName = userInfoProvided['firstName']
        except (KeyError) as e:
            errros['api.error.missing_firstname'] = "First name not provided"

        try:
            lastName = userInfoProvided['lastName']
        except (KeyError) as e:
            errros['api.error.missing_lastname'] = "Last name not provided"

        try:
            password = userInfoProvided['password']
        except (KeyError) as e:
            errros['api.error.missing_password'] = "Password not provided"

        try:
            confirmedPassword = userInfoProvided['confirmedPassword']
        except (KeyError) as e:
            errros['api.error.missing_confirmed_password'] = "Confirmed password not provided"

        try:
            phone1 = userInfoProvided['phone1']
        except (KeyError) as e:
            errros['api.error.missing_phone1'] = "Phone number 1 not provided"

        try:
            phone2 = userInfoProvided['phone2']
        except (KeyError) as e:
            phone2 = None


        try:
            province = userInfoProvided['province']
        except (KeyError) as e:
            errros['api.error.missing_province'] = "Province not provided"

        try:
            city = userInfoProvided['city']
        except (KeyError) as e:
            errros['api.error.missing_city'] = "City not provided"

        try:
            postalCode = userInfoProvided['postalCode']
        except (KeyError) as e:
            errros['api.error.missing_postalcode'] = "Postal code not provided"



        if len(errros) != 0:
            errorJson = json.dumps(errros)
            self.response.write(errorJson)
            self.response.set_status(400)
            return

        if password != confirmedPassword:
            errorJson = json.dumps({'api.error.password_mismatch' : 'Password \
                                        doesn\'t match confirmed password'})
            self.response.write(errorJson)
            self.response.set_status(400)
            return
        # TODO return error if password is not strong enough

        unique_properties = ['email_address']
        user_data = self.user_model.create_user(email, unique_properties, email_address=email,
              first_name=firstName, password_raw=password, phone1=phone1, phone2=phone2,
              province=province, city=city, last_name=lastName, verified=False, postal_code = postalCode)
        if not user_data[0]: # user_data is a tuple
            errorJson = json.dumps({'api.error.email_already_exists'
                                    : 'Email already exists'})
            self.response.write(errorJson)
            self.response.set_status(400)
            return

        user = user_data[1]
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        self.response.write(json.dumps({'token':token}))
        self.response.set_status(200)

        # verification_url = self.uri_for('verification', type='v', user_id=user_id,
        #                                 signup_token=token, _full=True)

        # msg = 'Send an email to user in order to verify their address. \
        #           They will be able to do so by visiting <a href="{url}">{url}</a>'

        # self.display_message(msg.format(url=verification_url))

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
            self.render_template('resetpassword.html', params)
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
    self.render_template('authenticated.html')


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
        self.render_template('forgot.html', params)
