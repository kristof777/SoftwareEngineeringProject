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
        self.render_template('../webpages/Create_User.html')

    def post(self):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')

        error_keys = ['email', 'firstName', 'lastName', 'password',
                      'confirmedPassword', 'phone1', 'province', 'city']
        error_values = [missing_email, missing_first_name, missing_last_name,
                        missing_password,missing_confirmed_password,
                        missing_phone_number,missing_province, missing_city]
        key_error_dict = dict(zip(error_keys, error_values))

        # validating if request has all required keys
        errors, values = keys_validation(key_error_dict, self.request.POST)
        phone2 = self.request.POST.get('phone2')

        # If there exists error then return the response, and stop the function
        if len(errors) != 0:
            error_json = json.dumps(errors)
            self.response.write(error_json)
            self.response.set_status(
                missing_invalid_parameter_error)
            return

        invalid = {}

        if not is_valid_phone(values['phone1']):
            invalid[invalid_phone1['error']] = "Invalid phone number 1"
        if phone2 is not None and not is_valid_phone(phone2):
            invalid[invalid_phone2['error']] = "Invalid phone number 2"
        if is_valid_email(values['email']):
            invalid[invalid_email['error']] = "Invalid email address"


        if len(invalid) != 0:
            error_json = json.dumps(invalid)
            self.response.write(error_json)
            self.response.set_status(
                missing_invalid_parameter_error)
            return

        if values['password'] != values['confirmedPassword']:
            error_json = json.dumps({
                password_mismatch['error']:
                    'Password does not match confirmed password'})
            self.response.write(error_json)
            self.response.set_status(missing_invalid_parameter_error)
            return

        password = values['password']
        if is_invalid_password(password):
            error_json = json.dumps({
                password_not_strong['error']: 'Password not strong enough'})
            self.response.write(error_json)
            self.response.set_status(missing_invalid_parameter_error)
            return

        unique_properties = ['email']
        user_data = self.user_model.create_user(
            values['email'], unique_properties, email=values['email'],
            first_name=values['firstName'],
            password_raw=password, phone1=values['phone1'], phone2=phone2,
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
        token = self.user_model.create_signup_token(user_id)
        self.response.write(json.dumps({'token': token, "userId": user_id}))
        self.response.set_status(success)


