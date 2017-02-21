import json
import Error_Code
from Base_Handler import *
import Main
import utils

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
        self.render_template('Create_User.html')

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


