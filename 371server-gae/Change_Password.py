import json
import logging

import Error_Code
from Base_Handler import *


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


class CreateUser(BaseHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
        @pre-cond: Expecting keys to be email, firstName, lastName,
                   password, confirmedPassword, phone1, phone2(optional),
                   city, postalCode. If any of these is not present an
                   appropriate error and status code 40 is returned.

                   password and ConfirmedPassword are expected to be equal then
                   if not then appropriate missing_invalid_parameter_error is
                   returned.

                   If email already exists, then an error is returned.
        @post-cond: An user with provided information is created in the
                    database. Token and userId is returned as an response
                    object.
    """
    def get(self):
        self.render_template('Chane_Password.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        errors = {}
        empty = u''

        #
        # For each required field, making sure it exists, is not empty
        # and also has something else other than spaces
        #

        email = self.request.POST.get('email')
        if email is None:
            errors[Error_Code.missing_email['error']] = "Email not provided"
        elif email.isspace() or email is empty:
            errors[Error_Code.missing_email['error']] = "Email not provided"
        first_name = self.request.POST.get('firstName')
        if first_name is None:
            errors[Error_Code.missing_first_name['error']] \
                = "First name not provided"
        elif first_name.isspace() or first_name is empty:
            errors[Error_Code.missing_first_name['error']] \
                = "First name not provided"

        last_name = self.request.POST.get('lastName')
        if last_name is None:
            errors[Error_Code.missing_last_name['error']] \
                = "Last name not provided"
        elif last_name.isspace() or last_name is empty:
            errors[Error_Code.missing_last_name['error']] \
                = "Last name not provided"

        password = self.request.POST.get('password')
        if password is None:
            errors[Error_Code.missing_password['error']] = \
                "Password not provided"
        elif password.isspace() or password is empty:
            errors[Error_Code.missing_password['error']] = \
                "Password not provided"

        confirmed_password = self.request.POST.get('confirmedPassword')
        if confirmed_password is None:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "Confirmed password not provided"
        elif confirmed_password.isspace() or confirmed_password is empty:
            errors[Error_Code.missing_confirmed_password['error']] \
                = "Confirmed password not provided"

        phone1 = self.request.POST.get('phone1')
        if phone1 is None:
            errors[Error_Code.missing_phone_number['error']] \
                = "Phone number 1 not provided"
        elif phone1.isspace() or phone1 is empty:
            errors[Error_Code.missing_phone_number['error']] \
                = "Phone number 1 not provided"

        province = self.request.POST.get('province')
        if province is None:
            errors[Error_Code.missing_province['error']] \
                = "Province not provided"
        elif province.isspace() or province is empty:
            errors[Error_Code.missing_province['error']] \
                = "Province not provided"

        city = self.request.POST.get('city')
        if city is None:
            errors[Error_Code.missing_city['error']] = "City not provided"
        elif city.isspace() or city is empty:
            errors[Error_Code.missing_city['error']] = "City not provided"

        postal_code = self.request.POST.get("postalCode")
        if postal_code is None:
            errors[Error_Code.missing_postal_code['error']] \
                = "Postal code not provided"
        elif postal_code.isspace() or postal_code is empty:
            errors[Error_Code.missing_postal_code['error']] \
                = "Postal code not provided"


        #
        # Done with required field checking
        #

        phone2 = self.request.POST.get('phone2')

        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(
                Error_Code.missing_invalid_parameter_error)
            return


        if password != confirmed_password:
            error_json = json.dumps(
                {Error_Code.password_mismatch
                 ['error']: 'Password does not match confirmed password'})

            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        password = str(password)
        if len(password)  < 8 \
            or not any(s.islower() for s in password) \
            or not any(s.isupper() for s in password) \
            or not any(s.isdigit() for s in password):
            error_json = json.dumps(
                {Error_Code.password_not_strong
                 ['error']: 'Password not strong enough'})
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return


        unique_properties = ['email']
        user_data = self.user_model.create_user(
            email, unique_properties, email=email, first_name=first_name,
            password_raw=password, phone1=phone1, phone2=phone2,
            province=province, city=city, last_name=last_name,
            verified=False, postal_code=postal_code)

        if not user_data[0]:  # user_data is a tuple
            error_json = json.dumps({Error_Code.email_alreadyExists['error']
                                    : 'Email already exists'})
            self.response.write(error_json)
            self.response.set_status(Error_Code.missing_invalid_parameter_error)
            return

        user = user_data[1]
        user_id = user.get_id()
        token = self.user_model.create_signup_token(user_id)

        self.response.write(json.dumps({'token': token, "userId": user_id}))
        self.response.set_status(Error_Code.success)


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
            self.render_template('Reset_Password.html', params)
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
    self.render_template('Authenticated.html')


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
        self.render_template('Forgot.html', params)
