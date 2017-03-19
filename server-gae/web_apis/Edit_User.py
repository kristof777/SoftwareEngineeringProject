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
    """

    def options(self, *args, **kwargs):
        setup_api_options(self)

    def get(self):
        self.render_template('../webpages/Edit_User.html')

    def post(self):
        setup_post(self.response)

        valid, values = \
            check_required_valid(edit_user_api, self.request.POST,
                                 self.response, True)

        if not valid:
            return

        change_values = json.loads(values['changeValues'])

        if len(change_values) == 0:
            write_error_to_response(self.response,
                                    {nothing_requested_to_change['error']:
                                         "Nothing requested to change"},
                                    nothing_requested_to_change['status'])
            return

        if "password" in change_values.keys():
            write_error_to_response(self.response,
                                    {password_cant_be_changed['error']:
                                         "Please don't change password using edit user"},
                                    password_cant_be_changed['status'])
            return

        if any(key not in ["phone1", "phone2", "email", "province", "city",
                           "firstName", "lastName"] for key in
               change_values.keys()):
            write_error_to_response(self.response, {unrecognized_key['error']:
                                                        "Unrecognized key found"},
                                    unrecognized_key['status'])
            return

        user = User.get_by_id(int(values["userId"]))
        for key in change_values:
            user.set_property(key, change_values[key])
        user.put()
        write_success_to_response(self.response, {})
