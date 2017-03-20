import sys
sys.path.append("../")
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from extras.Base_Handler import BaseHandler
from extras.Utils import *
from models.User import User
from API_NAME import edit_user_api
from extras.Required_Fields import check_required_valid


class EditUser(BaseHandler):
    """
       Class used to handle get and post.
       Get:  is used to render an HTML page.
       Post:
           @pre-cond: Expecting keys to be changeValues, userId, authToken.
                      If any of these is not present an appropriate error and
                      status code is returned in the response..
                      changeValues can only have keys that are associated with
                      User model otherwise an error is returned in the response.
                      edit user cannot be used to change the password, if tried
                      an error is returned in the response.
                      If email is changed then email is set to be not verified.

           @post-cond: Using userId and authToken,a user is found, and it's
                       information is updated using changeValues dictionary.

           @return: Nothing

       """
    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(edit_user_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        change_values = json.loads(values['changeValues'])

        if len(change_values) == 0:
            error = {nothing_requested_to_change['error']:
                         "Nothing requested to change"}
            write_error_to_response(self.response, error,
                                    nothing_requested_to_change['status'])
            return

        if "password" in change_values.keys():
            error = {password_cant_be_changed['error']:
                         "Please don't change password using edit user"}

            write_error_to_response(self.response, error,
                                    password_cant_be_changed['status'])
            return

        if any(key not in ["phone1", "phone2", "email", "province", "city",
                           "firstName", "lastName"]
               for key in change_values.keys()):
            write_error_to_response(
                self.response,
                {unrecognized_key['error']: "Unrecognized key found"},
                unrecognized_key['status'])
            return

        user = User.get_by_id(int(values["userId"]))

        assert user is not None

        for key in change_values:
            user.set_property(key, change_values[key])
        user.put()
        write_success_to_response(self.response, {})
