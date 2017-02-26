import sys
sys.path.append("../")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import json
from extras.Base_Handler import BaseHandler
from extras.Error_Code import *
from extras.utils import *


class CreateUser(BaseHandler):
    """
    Class used to handle get and post.
    Get:  is used to render an HTML page.
    Post:
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
    """
    def get(self):
        self.render_template('../webpages/Create_User.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        error_keys = ['email', 'firstName', 'password',
                      'confirmedPassword', 'phone1', 'province', 'city']

        # validating if request has all required keys
        errors, values = keys_missing(error_keys, self.request.POST)
        phone2 = self.request.POST.get('phone2')
        if not is_missing(phone2):
            values['phone2'] = phone2

        last_name = self.request.POST.get('lastName')
        if not is_missing(last_name):
            values['lastName'] = last_name

        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            write_error_to_response(self.response, errors, missing_invalid_parameter_error)
            return

        invalid = key_validation(values)

        if len(invalid) != 0:
            write_error_to_response(self.response, invalid, missing_invalid_parameter_error)
            return

        if values['password'] != values['confirmedPassword']:
            error = {
                password_mismatch['error']:
                    'Password does not match confirmed password'}
            write_error_to_response(self.response, error, missing_invalid_parameter_error)

            return

        values['province'] = scale_province(str(values['province']))
        unique_properties = ['email']
        user_data = self.user_model.create_user(
            values['email'], unique_properties, email=values['email'],
            first_name=values['firstName'],
            password_raw=values['password'], phone1=values['phone1'], phone2=phone2,
            province=values['province'], city=values['city'],
            last_name=values['lastName'],
            verified=False)

        # user_data[0] contains True if user was created successfully
        if not user_data[0]:
            error_json = json.dumps({email_alreadyExists['error']
                                    : 'Email already exists'})
            self.response.write(error_json)
            self.response.set_status(missing_invalid_parameter_error)

            return

        # user_data[1] contains Token if user was created successfully
        user = user_data[1]
        user_id = user.get_id()
        signup_token = self.user_model.create_signup_token(user_id)
        token = self.user_model.create_auth_token(user_id)

        self.auth.get_user_by_token(user_id, token, remember=True,
                                    save_session=True)

        write_success_to_response(self.response, {'signupToken': signup_token,
                                                  'token': token,
                                                  "userId": user_id})


